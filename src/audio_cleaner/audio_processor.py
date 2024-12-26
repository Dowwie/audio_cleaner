import time
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from typing import Union, Tuple, Optional
from loguru import logger


class AudioProcessor:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        logger.debug(f"Initialized AudioProcessor with sample rate {sample_rate}Hz")

    def load_audio(self, file_path: Union[str, Path]) -> Tuple[np.ndarray, int]:
        """Load an audio file and return the signal and sample rate."""
        logger.info(f"Loading audio file: {file_path}")
        try:
            signal, sr = librosa.load(file_path, sr=self.sample_rate)
            duration = len(signal) / sr
            logger.info(
                f"Loaded audio file: duration={duration:.2f}s, sample_rate={sr}Hz"
            )
            logger.debug(
                f"Signal shape={signal.shape}, min={signal.min():.3f}, max={signal.max():.3f}"
            )
            return signal, sr
        except Exception as e:
            logger.error(f"Failed to load audio file {file_path}: {str(e)}")
            raise

    def reduce_noise(
        self,
        signal: np.ndarray,
        noise_reduce_factor: float = 0.8,
        noise_sample_duration: float = 2.0,
    ) -> np.ndarray:
        """
        Reduce background noise in the audio signal.

        Args:
            signal: Input audio signal
            noise_reduce_factor: Factor for noise reduction (0 to 1)
            noise_sample_duration: Duration in seconds to sample for noise profile

        Returns:
            Processed audio signal with reduced noise
        """
        logger.info(f"Starting noise reduction with factor={noise_reduce_factor}")

        # Calculate noise profile
        noise_sample_size = int(noise_sample_duration * self.sample_rate)
        noise_sample = signal[:noise_sample_size]
        logger.debug(
            f"Using first {noise_sample_duration}s ({noise_sample_size} samples) for noise profile"
        )

        # Compute spectral representation
        logger.debug("Computing STFT of noise sample")
        noise_profile = np.mean(np.abs(librosa.stft(noise_sample)), axis=1)
        logger.debug(f"Noise profile shape={noise_profile.shape}")

        # Process full signal
        logger.debug("Computing STFT of full signal")
        D = librosa.stft(signal)
        logger.debug(f"STFT shape={D.shape}")

        mag, phase = librosa.magphase(D)
        logger.debug(f"Magnitude range: {mag.min():.3f} to {mag.max():.3f}")

        # Apply noise reduction
        logger.debug("Applying noise reduction")
        mag_reduced = np.maximum(
            0, mag - noise_reduce_factor * noise_profile[:, np.newaxis]
        )
        logger.debug(
            f"Reduced magnitude range: {mag_reduced.min():.3f} to {mag_reduced.max():.3f}"
        )

        # Reconstruct signal
        logger.debug("Reconstructing signal")
        D_reduced = mag_reduced * phase
        processed = librosa.istft(D_reduced)

        # Log reduction stats
        original_power = np.mean(signal**2)
        processed_power = np.mean(processed**2)
        reduction_db = 10 * np.log10(original_power / processed_power)
        logger.info(
            f"Noise reduction complete. Average power reduction: {reduction_db:.1f}dB"
        )

        return processed

    def save_audio(
        self,
        signal: np.ndarray,
        output_path: Union[str, Path],
        sample_rate: Optional[int] = None,
    ) -> None:
        """
        Save the processed audio to a file.

        Args:
            signal: Audio signal to save
            output_path: Path to save the audio file
            sample_rate: Optional sample rate (defaults to self.sample_rate)
        """
        if sample_rate is None:
            sample_rate = self.sample_rate

        output_path = Path(output_path)
        logger.info(f"Saving audio to {output_path}")
        logger.debug(
            f"Signal stats: shape={signal.shape}, min={signal.min():.3f}, max={signal.max():.3f}"
        )

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            sf.write(str(output_path), signal, sample_rate)
            file_size = output_path.stat().st_size
            logger.info(f"Saved audio file: size={file_size/1024/1024:.1f}MB")
        except Exception as e:
            logger.error(f"Failed to save audio to {output_path}: {str(e)}")
            raise

    def process_file(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        noise_reduce_factor: float = 0.8,
    ) -> None:
        """
        Process an entire audio file and save the result.

        Args:
            input_path: Path to input audio file
            output_path: Path to save processed audio
            noise_reduce_factor: Factor for noise reduction (0 to 1)
        """
        logger.info(f"Processing audio file: {input_path} -> {output_path}")

        try:
            # Load
            start_time = time.time()
            signal, sr = self.load_audio(input_path)
            load_time = time.time() - start_time
            logger.debug(f"Loading completed in {load_time:.2f}s")

            # Process
            start_time = time.time()
            processed_signal = self.reduce_noise(signal, noise_reduce_factor)
            process_time = time.time() - start_time
            logger.debug(f"Processing completed in {process_time:.2f}s")

            # Save
            start_time = time.time()
            self.save_audio(processed_signal, output_path, sr)
            save_time = time.time() - start_time
            logger.debug(f"Saving completed in {save_time:.2f}s")

            total_time = load_time + process_time + save_time
            logger.success(
                f"Successfully processed audio file in {total_time:.2f}s "
                f"(load={load_time:.2f}s, process={process_time:.2f}s, save={save_time:.2f}s)"
            )
        except Exception as e:
            logger.exception("Failed to process audio file")
            raise
