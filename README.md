# Audio Cleaner

Clean background noise from audio files using spectral subtraction.

## Installation

```bash
# Install using pipx (recommended)
pipx install git+https://github.com/Dowwie/audio-cleaner.git

# Or install using pip
pip install git+https://github.com/Dowwie/audio-cleaner.git
```

## Usage

After installation, the `audio-cleaner` command will be available in your system:

```bash
# Basic usage
audio-cleaner input.mp3 output.mp3

# Adjust noise reduction strength (0.0 to 1.0)
audio-cleaner input.mp3 output.mp3 -f 0.6

# Change noise sample duration
audio-cleaner input.mp3 output.mp3 -d 3.0

# Specify custom sample rate
audio-cleaner input.mp3 output.mp3 -s 48000

# See all options
audio-cleaner --help
```

### Command Line Options

```
Positional Arguments:
  input_file            Input audio file path
  output_file          Output audio file path

Optional Arguments:
  -h, --help           Show this help message and exit
  -f, --noise-factor   Noise reduction factor (0.0 to 1.0, default: 0.8)
  -d, --duration       Duration in seconds to sample for noise profile (default: 2.0)
  -s, --sample-rate    Sample rate in Hz (default: 44100)
  --log-file          Path to log file (default: logs/audio_cleaner.log)
```

### Tips for Best Results

1. Ensure the beginning of your audio file contains a few seconds of "silence" with only the background noise you want to remove
2. Start with the default noise factor (0.8) and adjust if needed:
   - Increase for more aggressive noise removal
   - Decrease if the audio sounds distorted
3. Use the debug logs to monitor the noise reduction process:
   ```bash
   audio-cleaner input.mp3 output.mp3 --log-file process.log
   ```

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/audio-cleaner.git
cd audio-cleaner

# Create and activate virtual environment using uv
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.\.venv\Scripts\activate  # On Windows

# Install in development mode with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest
```

## How It Works

This noise reduction tool works by analyzing and removing consistent background noise from audio recordings. The process begins by examining a sample of the background noise, typically taken from the first few seconds of the recording where there's relative silence. This sample is used to create a "noise profile" that characterizes the unwanted background sounds.

The core of the process uses spectral analysis through the Short-Time Fourier Transform (STFT), which converts the audio from a time-based signal into a frequency-based representation. This transformation allows us to see how different frequencies contribute to the overall sound at each moment. By analyzing the noise sample in this frequency domain, we can identify which frequencies are predominantly associated with the background noise.

The actual noise reduction happens by subtracting this noise profile from the entire recording's frequency representation, scaled by a configurable factor. This factor determines how aggressively the noise is reduced – higher values remove more noise but might affect the desired audio content, while lower values are more conservative but may leave more noise intact. After subtracting the noise profile, the program reconstructs the audio signal using the Inverse Short-Time Fourier Transform (ISTFT), maintaining the original phase information to preserve audio quality.

The effectiveness of the noise reduction depends on several factors, particularly how consistent the background noise is throughout the recording and whether the initial noise sample accurately represents the unwanted sounds. The tool works best with steady, consistent background noise like computer fans, air conditioning, or room tone, and may be less effective with variable or intermittent noise.