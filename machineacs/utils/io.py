from pathlib import Path
from typing import Dict, Any, List, Optional
import aiofiles
import aiofiles.os

from cleaner import clean_file


async def populate(
    config: Dict[str, Any],
    files: Optional[List[tuple]] = None
):
    items_generator = clean_file(config, files)
    files_for_download = await file_writer(items_generator)
    return files_for_download
    

async def file_writer(generator):
    open_files: Dict[Path, Any] = {}
    files_for_download = []

    try:
        async for output, file_name, path, kind in generator:
            if file_name not in files_for_download and path not in files_for_download:
                files_for_download.append((file_name, path))
            if path not in open_files:
                parent_dir = str(Path(path).parent)
                await aiofiles.os.makedirs(parent_dir, exist_ok=True)
                f = await aiofiles.open(path, "w", encoding="utf-8", buffering=1)
                open_files[path] = f

            f = open_files[path]
            await f.write(output)
            await f.flush()
    finally:
        for f in open_files.values():
            await f.close()
    return files_for_download
