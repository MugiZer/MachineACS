import json
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Union, Generator, List, AsyncGenerator

import aiofiles
import ijson

from config.registry import apply_filters
from utils.logger import logger
from adapters.canonicalizer import Canonicalizer
from filters.schema_coercer import coerce_schema
from filters.tokens import (
    Token, Line, StructuralToken, StringValueToken, KeyToken,
    NumberToken, BoolNullToken, NewlineToken, HashToken, RuleToken
)


async def stream_json_as_tokens(
    file_path: Union[str, Path]
) -> AsyncGenerator[Token, None]:
    """
    Stream a JSON file as tokens for processing.

    Args:
        file_path: Path to the JSON file.

    Yields:
        Token objects representing the JSON structure and values.
    """
    async with aiofiles.open(file_path, "rb") as input_file:
        yield StructuralToken("[")
        first = True

        try:
            parser = ijson.items_async(input_file, "item")
            async for item in parser:
                if not first:
                    yield StructuralToken(",")
                first = False

                dict_hash_val = Canonicalizer.canonicalize(item)
                yield HashToken(dict_hash_val)

                # Feed the raw tokens from traverse_obj through our new schema coercer pipeline
                raw_tokens = _traverse_obj(item)
                coerced_tokens = coerce_schema(raw_tokens)
                
                for token in coerced_tokens:
                    yield token
            
            yield StructuralToken("]")

        except ijson.common.IncompleteJSONError as e:
            logger.warning(f"Incomplete JSON in {file_path}: {e}")


async def stream_jsonl_as_tokens(
    file_path: Union[str, Path]
) -> AsyncGenerator[Token, None]:
    """
    Stream a JSONL file as tokens for processing.

    Args:
        file_path: Path to the JSONL file.

    Yields:
        Token objects representing each JSON line's structure and values.
    """
    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        line_num = 0
        async for line in f:
            line_num += 1
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
                hash_val = Canonicalizer.canonicalize(data)
                yield HashToken(hash_val)

                raw_tokens = _traverse_obj(data)
                coerced_tokens = coerce_schema(raw_tokens)
                
                for token in coerced_tokens:
                    yield token

                yield NewlineToken()

            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON at line {line_num} in {file_path}: {e}")


def _traverse_obj(obj: Any) -> Generator[Token, None, None]:
    """
    Recursively traverse a Python object and yield tokens.

    Args:
        obj: The Python object to traverse.

    Yields:
        Token objects representing the object's structure and values.
    """
    if isinstance(obj, dict):
        yield StructuralToken("{")
        first = True
        for k, v in obj.items():
            if not first:
                yield StructuralToken(",")
            first = False
            yield KeyToken(k)
            yield from _traverse_obj(v)
        yield StructuralToken("}")
    elif isinstance(obj, list):
        yield StructuralToken("[")
        first = True
        for item in obj:
            if not first:
                yield StructuralToken(",")
            first = False
            yield from _traverse_obj(item)
        yield StructuralToken("]")
    elif isinstance(obj, str):
        yield StringValueToken(obj)
    elif isinstance(obj, bool) or obj is None:
        yield BoolNullToken(obj)
    elif isinstance(obj, (int, float, Decimal)):
        yield NumberToken(obj)
