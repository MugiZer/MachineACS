import json
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Union, Generator, List, AsyncGenerator

import aiofiles
import ijson

from config.registry import apply_filters
from utils.logger import logger

from adapters.canonicalizer import Canonicalizer 


class Token:
    """Base token class for polymorphic processing."""

    def __init__(self, content: Any) -> None:
        self.content = content

    def clean(self, config: Dict[str, Any]) -> Any:
        """Apply filters to the token content."""
        return apply_filters(self.content, config)

    def serialize(self, cleaned: Any) -> str:
        """Serialize the cleaned content to string."""
        return str(cleaned)

    def process(self, config: Dict[str, Any]) -> str:
        """Clean and serialize the token."""
        return self.serialize(self.clean(config))


class Line(Token):
    """Token representing a line of text."""

    def serialize(self, cleaned: str) -> str:
        return cleaned + "\n"


class StructuralToken(Token):
    """Token for JSON structural characters (braces, brackets, commas)."""

    def clean(self, config: Dict[str, Any]) -> str:
        return str(self.content)

    def serialize(self, cleaned: str) -> str:
        return cleaned


class StringValueToken(Token):
    """Token for JSON string values."""

    def serialize(self, cleaned: str) -> str:
        return json.dumps(cleaned, ensure_ascii=False)


class KeyToken(Token):
    """Token for JSON object keys."""

    def serialize(self, cleaned: str) -> str:
        return json.dumps(cleaned, ensure_ascii=False) + ":"


class NumberToken(Token):
    """Token for JSON number values."""

    def clean(self, config: Dict[str, Any]) -> Union[Decimal, int, float]:
        return self.content

    def serialize(self, cleaned: Union[Decimal, int, float]) -> str:
        if isinstance(cleaned, Decimal):
            return str(cleaned)
        return json.dumps(cleaned)


class BoolNullToken(Token):
    """Token for JSON boolean and null values."""

    def clean(self, config: Dict[str, Any]) -> Any:
        return self.content

    def serialize(self, cleaned: Any) -> str:
        return json.dumps(cleaned)


class NewlineToken(Token):
    """Token representing a newline character."""

    def __init__(self) -> None:
        super().__init__("\n")

    def clean(self, config: Dict[str, Any]) -> str:
        return str(self.content)

    def serialize(self, cleaned: str) -> str:
        return cleaned

class HashToken(Token):
    #token to represent the before_hash so it can get processed distinctly from the other tokens, it needs to come out exactly as it came in 
    def __init__(self, content: str) -> None:
        super().__init__(content)

    def clean(self, config: Dict[str, Any]) -> str:
        return self.content
    
    def serialize(self, cleaned: str) -> str:
        return cleaned
        

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

                hash_val = Canonicalizer.canonicalize(item)
                yield HashToken(hash_val)

                for token in _traverse_obj(item):
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
                #hash the json object
                hash = Canonicalizer.canonicalize(data)
                yield HashToken(hash)

                for token in _traverse_obj(data):
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
    elif isinstance(obj, (int, float)):
        yield NumberToken(obj)
