"""
Nexus AI Assistant Package
A powerful AI assistant with self-learning capabilities for natural language processing and task automation.
"""

__version__ = "2.0.0"
__author__ = "İlker Atagün"
__email__ = "ilker@nexus-ai.com"

from .core.assistant import AIAssistant
from .core.config import Config
from .core.learning import SelfImprovementEngine, LearningDatabase
from .utils.logger import setup_logger

__all__ = ["AIAssistant", "Config", "SelfImprovementEngine", "LearningDatabase", "setup_logger"]
