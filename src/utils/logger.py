"""Structured logging configuration for ADM."""

import logging
import sys
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels."""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{self.BOLD}{levelname}{self.RESET}"
            )

        # Format the message
        formatted = super().format(record)

        return formatted


def setup_logger(name: str = "adm", level: str = "INFO", verbose: bool = False) -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        verbose: If True, set level to DEBUG

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Set level
    if verbose:
        level = "DEBUG"
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Format: [LEVEL] message
    formatter = ColoredFormatter(
        fmt="%(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance. If no name provided, returns the root ADM logger.

    Args:
        name: Optional logger name (will be prefixed with 'adm.')

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"adm.{name}")
    return logging.getLogger("adm")
