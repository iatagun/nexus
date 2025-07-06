"""
Nexus AI Assistant Package
A powerful AI assistant for natural language processing and task automation.
"""

__version__ = "1.0.0"
__author__ = "Nexus Team"
__email__ = "support@nexus-ai.com"

from .core.assistant import AIAssistant
from .core.config import Config
from .utils.logger import setup_logger

__all__ = ["AIAssistant", "Config", "setup_logger"]
