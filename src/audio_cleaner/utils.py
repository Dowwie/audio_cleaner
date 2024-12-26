from pathlib import Path
from typing import Union


def validate_audio_file(file_path: Union[str, Path]) -> bool:
    """Validate that the file exists and has a supported audio extension."""
    path = Path(file_path)
    supported_extensions = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
    return path.exists() and path.suffix.lower() in supported_extensions


def ensure_directory(dir_path: Union[str, Path]) -> None:
    """Ensure that the directory exists, create if it doesn't."""
    Path(dir_path).mkdir(parents=True, exist_ok=True)
