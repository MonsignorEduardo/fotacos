"""Logging configuration for fotacos using Loguru."""

import logging
import sys
from pathlib import Path

from loguru import logger

from fotacos.env import get_settings

settings = get_settings()


class InterceptHandler(logging.Handler):
    """Intercept standard logging and redirect to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record to Loguru."""
        # Get corresponding Loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller to get correct stack depth
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_back and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """Configure logging for the application."""
    # Remove default handler
    logger.remove()

    # Configure Loguru
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Add file handler with rotation and compression
    logger.add(
        log_dir / "application.log",
        rotation="500 MB",
        compression="zip",
        level="INFO",
        backtrace=True,
        diagnose=True,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        enqueue=True,  # Async logging for better performance
    )

    # Add console handler for development
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG" if settings.debug else "INFO",
        colorize=True,
    )

    # Add error-specific log file
    logger.add(
        log_dir / "errors.log",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        level="ERROR",
        backtrace=True,
        diagnose=True,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    # Ensure loggers propagate to root logger
    loggers_to_intercept = (
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "asyncio",
        "starlette",
        "multipart",
    )

    for logger_name in loggers_to_intercept:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = []
        logging_logger.propagate = True

    logger.info("Logging configured successfully")
