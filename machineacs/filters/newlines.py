from typing import AsyncGenerator, Any, Tuple, Optional


async def newlines(
    generator: AsyncGenerator[Tuple[str, str, Any, str], None]
) -> AsyncGenerator[Tuple[str, str, Any, str], None]:
    """
    Filter that collapses consecutive empty lines into a single empty line.

    Args:
        generator: Async generator yielding (line, filename, path, kind) tuples.

    Yields:
        Filtered line data tuples with consecutive empty lines collapsed.
    """
    last_was_empty = False
    current_file: Optional[str] = None

    async for line_data in generator:
        line, file_name, _, _ = line_data

        if file_name != current_file:
            last_was_empty = False
            current_file = file_name

        is_empty = not line.strip()

        if is_empty and last_was_empty:
            continue

        yield line_data
        last_was_empty = is_empty
