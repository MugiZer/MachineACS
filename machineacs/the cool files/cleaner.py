import os
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, AsyncGenerator, Tuple
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from adapters.format import collect_gen, FileInfo
from filters.newlines import newlines as newline_filter
from filters.tokens import Token, HashToken, RuleToken

DATA_DIR = Path(__file__).resolve().parent / "data"


async def _batch_items(
    gen: AsyncGenerator,
    batch_size: int = 1000
) -> AsyncGenerator[List[Any], None]:

    batch: List[Any] = []
    async for item in gen:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def _process_token(token: Token, config: Dict[str, Any]) -> str:
    return token.process(config)

async def clean_line(
    generators: AsyncGenerator,
    config: Dict[str, Any]
) -> AsyncGenerator[Tuple[str, str, Path, str], None]:

    batch_size = 100 if config.get("filters", {}).get("grammar") else 1000
    max_workers = os.cpu_count()

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        async for gen, file_name, file_path, kind in generators:
            if not file_path or not file_path.exists():
                continue

            new_file = f"cleaned_{Path(file_name).name}"
            new_file_path = DATA_DIR / new_file
            new_file_path.parent.mkdir(parents=True, exist_ok=True)

            file_config = {**config, "file_type": kind}
            
            accumulation_buffer = []
            current_dict_job_id = None

            async for batch in _batch_items(gen, batch_size=batch_size):
                
                normal_tokens = []
                batch_job_id = config.get("job_id")  # This is the encompassing parent batch_id
                
                for token in batch:
                    if isinstance(token, HashToken):
                        hash_value = token.content
                        if batch_job_id:
                            # Generate a unique job ID for this specific dictionary
                            dict_job_id = str(uuid.uuid4())
                            
                            # Log that this dictionary started processing
                            from datetime import datetime
                            from database import register_dictionary_job, insert_before_hash_value
                            register_dictionary_job(
                                job_id=dict_job_id,
                                batch_id=batch_job_id, 
                                status="processing", 
                                time=datetime.now().isoformat()
                            )
                            
                            # Link the Canonicalized JSON hash to this dictionary job
                            insert_before_hash_value(dict_job_id, hash_value)
                            
                            # Add boundary so we can compute the after_hash
                            normal_tokens.append(("HASH_BOUNDARY", dict_job_id))
                    else:
                        normal_tokens.append(token)
                
                if normal_tokens:
                    # Filter out our injected tuples before passing to the executor
                    tokens_to_process = [t for t in normal_tokens if not isinstance(t, tuple)]
                    results_iterator = executor.map(_process_token, tokens_to_process, repeat(file_config))
                    # Consume to a list so we can iterate by index
                    results_list = list(results_iterator)
                    
                    result_idx = 0
                    
                    for item in normal_tokens:
                        if isinstance(item, tuple) and item[0] == "HASH_BOUNDARY":
                            new_dict_job_id = item[1]
                            # If we were tracking a previous dictionary, process it now
                            if current_dict_job_id and accumulation_buffer:
                                dict_str = "".join(accumulation_buffer).strip()
                                # Clean up structural JSON array tokens from the string wrapper
                                if dict_str.startswith("["): dict_str = dict_str[1:].strip()
                                if dict_str.startswith(","): dict_str = dict_str[1:].strip()
                                if dict_str.endswith("]"): dict_str = dict_str[:-1].strip()
                                if dict_str.endswith(","): dict_str = dict_str[:-1].strip()
                                
                                if dict_str:
                                    try:
                                        import json
                                        from adapters.canonicalizer import Canonicalizer
                                        from database import update_after_hash_value
                                        parsed_dict = json.loads(dict_str)
                                        after_hash = Canonicalizer.canonicalize(parsed_dict)
                                        update_after_hash_value(current_dict_job_id, after_hash)
                                    except Exception as e:
                                        print(f"Failed to post-hash dict: {e}")
                            
                            # Reset buffer for the new dictionary
                            accumulation_buffer = []
                            current_dict_job_id = new_dict_job_id
                        else:
                            cleaned_val = results_list[result_idx]
                            
                            # If it's a RuleToken (empty string yielded via _process_token but we need the raw item)
                            # Actually, _process_token returns string. We need to check the original token type!
                            if isinstance(item, RuleToken):
                                rule_data = item.content
                                if current_dict_job_id:
                                    from database import insert_rule_log
                                    insert_rule_log(
                                        job_id=current_dict_job_id,
                                        rule_type=rule_data.get("rule_type", "Unknown"),
                                        key_name=rule_data.get("key", "N/A"),
                                        before=rule_data.get("before", ""),
                                        after=rule_data.get("after", "")
                                    )
                                # Don't yield RuleTokens to the file
                            else:
                                accumulation_buffer.append(cleaned_val)
                                yield cleaned_val, new_file, new_file_path, kind
                            
                            result_idx += 1

            # Flush the final dictionary out of the buffer when the batch loop finishes
            if current_dict_job_id and accumulation_buffer:
                dict_str = "".join(accumulation_buffer).strip()
                if dict_str.startswith("["): dict_str = dict_str[1:].strip()
                if dict_str.startswith(","): dict_str = dict_str[1:].strip()
                if dict_str.endswith("]"): dict_str = dict_str[:-1].strip()
                if dict_str.endswith(","): dict_str = dict_str[:-1].strip()
                
                if dict_str:
                    try:
                        import json
                        from adapters.canonicalizer import Canonicalizer
                        from database import update_after_hash_value
                        parsed_dict = json.loads(dict_str)
                        after_hash = Canonicalizer.canonicalize(parsed_dict)
                        update_after_hash_value(current_dict_job_id, after_hash)
                    except Exception as e:
                        print(f"Failed to post-hash final dict: {e}")


async def clean_file(
    config: Dict[str, Any],
    files: Optional[List[FileInfo]] = None
) -> AsyncGenerator[Tuple[str, str, Path, str], None]:

    raw_gen = collect_gen(files)
    pipeline = clean_line(raw_gen, config)

    if config.get("newlines"):
        pipeline = newline_filter(pipeline)

    async for item in pipeline:
        yield item

    from filters.grammar import save_cache
    save_cache()
