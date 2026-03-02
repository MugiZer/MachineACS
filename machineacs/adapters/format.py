from pathlib import Path
from typing import Dict, Any, Type, Optional, AsyncGenerator, Tuple, List

import aiofiles

from filters.json_structurer import (
    Token,
    Line,
    stream_json_as_tokens,
    stream_jsonl_as_tokens
)

FileInfo = Tuple[str, str, str]  # (kind, filename, path)

class BaseYielder:
    
    @staticmethod
    async def yield_gen(file_path: Path) -> AsyncGenerator[Token, None]:
        raise NotImplementedError


class CSVYielder(BaseYielder):

    @staticmethod
    async def yield_gen(file_path: Path) -> AsyncGenerator[Line, None]:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            async for line in f:
                yield Line(line.rstrip("\n"))


class TXTYielder(BaseYielder):

    @staticmethod
    async def yield_gen(file_path: Path) -> AsyncGenerator[Line, None]:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            async for line in f:
                yield Line(line.rstrip("\n"))


class JSONYielder(BaseYielder):

    @staticmethod
    async def yield_gen(file_path: Path) -> AsyncGenerator[Token, None]:
        async for token in stream_json_as_tokens(file_path):
            yield token


class JSONLYielder(BaseYielder):
    @staticmethod
    async def yield_gen(file_path: Path) -> AsyncGenerator[Token, None]:
        async for token in stream_jsonl_as_tokens(file_path):
            yield token


YIELDERS: Dict[str, Type[BaseYielder]] = {
    "csv": CSVYielder,
    "txt": TXTYielder,
    "json": JSONYielder,
    "jsonl": JSONLYielder,
}


async def collect_gen(
    files: Optional[List[FileInfo]] = None
) -> AsyncGenerator[Tuple[Any, str, Path, str], None]:
    if files is None:
        return

    for kind, file_name, path_str in files:
        file_path = Path(path_str)

        if not file_path.exists():
            continue

        yielder_class = YIELDERS.get(kind)
        if not yielder_class:
            continue

        gen = yielder_class.yield_gen(file_path)
        yield gen, file_name, file_path, kind
