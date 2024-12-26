import pytest
import numpy as np
from pathlib import Path

# Import directly from package, not from src
from audio_cleaner.audio_processor import AudioProcessor
from audio_cleaner.utils import validate_audio_file


def test_audio_processor_initialization():
    processor = AudioProcessor()
    assert processor.sample_rate == 44100


def test_validate_audio_file(tmp_path):
    # Use pytest's tmp_path fixture instead of hardcoded paths
    test_file = tmp_path / "sample.mp3"
    test_file.touch()  # Create empty file
    assert validate_audio_file(test_file) == True

    non_existent = tmp_path / "non_existent.mp3"
    assert validate_audio_file(non_existent) == False
