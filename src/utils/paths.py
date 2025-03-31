from pathlib import Path
from tempfile import mkstemp

__all__ = ["ROOT", "tmp_path"]

ROOT = Path(__file__).parent.parent.parent
"""The root directory of the project"""


def tmp_path(prefix: str | None = None, suffix: str | None = None) -> Path:
    """Create a temporary file path"""
    return Path(mkstemp(prefix=prefix, suffix=suffix)[1]).resolve()
