import sys
from pathlib import Path
from loguru import logger


def setup_logging(
    level="INFO", log_file: Path | None = None, rotation="10 MB", retention="1 week"
):
    """Configure logging for the application.

    Args:
        level: Log level for console output
        log_file: Optional path to log file
        rotation: When to rotate log file
        retention: How long to keep log files
    """
    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
    )

    # Add file handler if requested
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(log_file),
            rotation=rotation,
            retention=retention,
            level="DEBUG",  # File logging can be more verbose
        )
