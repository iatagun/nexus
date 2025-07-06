"""
Logging utilities for Nexus AI Assistant
"""

import sys
from loguru import logger
from rich.console import Console
from rich.logging import RichHandler
from ..core.config import config


def setup_logger(name: str = "nexus") -> logger:
    """
    Set up logging with rich formatting
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    # Remove default handler
    logger.remove()
    
    # Console handler with rich formatting
    console = Console()
    
    logger.add(
        RichHandler(console=console, rich_tracebacks=True),
        level=config.log_level.upper(),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        colorize=True,
    )
    
    # File handler for persistent logging
    logger.add(
        "logs/nexus.log",
        rotation="1 day",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    
    return logger


# Global logger instance
nexus_logger = setup_logger()
