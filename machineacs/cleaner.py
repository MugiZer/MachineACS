import os
from pathlib import Path
from typing import List, Dict, Any, Optional, AsyncGenerator, Tuple
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from adapters.format import collect_gen, FileInfo
from filters.newlines import newlines as newline_filter
from utils.json_structurer import Token

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

            async for batch in _batch_items(gen, batch_size=batch_size):
                results = executor.map(_process_token, batch, repeat(file_config))
                for line in results:
                    yield line, new_file, new_file_path, kind


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
