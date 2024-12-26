#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from loguru import logger

from .audio_processor import AudioProcessor
from .log import setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audio Cleaner - Remove background noise from audio files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required arguments
    parser.add_argument("input_file", type=Path, help="Input audio file path")
    parser.add_argument("output_file", type=Path, help="Output audio file path")

    # Optional arguments
    parser.add_argument(
        "-f",
        "--noise-factor",
        type=float,
        default=0.8,
        help="Noise reduction factor (0.0 to 1.0)",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        default=2.0,
        help="Duration in seconds to sample for noise profile",
    )
    parser.add_argument(
        "-s", "--sample-rate", type=int, default=44100, help="Sample rate in Hz"
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("logs/audio_cleaner.log"),
        help="Path to log file",
    )

    args = parser.parse_args()

    # Validate input file exists
    if not args.input_file.exists():
        parser.error(f"Input file does not exist: {args.input_file}")

    # Ensure output directory exists
    args.output_file.parent.mkdir(parents=True, exist_ok=True)

    return args


def main() -> int:
    """Main entry point for the application."""
    try:
        args = parse_args()

        # Set up logging with DEBUG level
        setup_logging(level="DEBUG", log_file=args.log_file)

        logger.info("Starting Audio Cleaner")
        logger.debug(f"Arguments: {args}")

        # Initialize processor
        processor = AudioProcessor(sample_rate=args.sample_rate)

        # Process file
        processor.process_file(
            input_path=args.input_file,
            output_path=args.output_file,
            noise_reduce_factor=args.noise_factor,
        )

        logger.info("Audio Cleaner completed successfully")
        return 0

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        return 130
    except Exception as e:
        logger.exception("An error occurred")
        return 1


if __name__ == "__main__":
    sys.exit(main())
