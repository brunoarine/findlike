from pathlib import Path
import os

def get_relative_path(source: Path, target: Path) -> Path:
    """Get the relative path to target from a source.

    Args:
        source (Path): path to the reference filename.
        target (Path): path to the target.

    Returns:
        A Path object in relative path format.
    """
    return Path(os.path.relpath(target, source.parent))

