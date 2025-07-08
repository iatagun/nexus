"""
Configuration management for Nexus AI Assistant
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    """Application configuration"""
    
    # Model Provider Configuration
    model_provider: str = Field("ollama", env="MODEL_PROVIDER")  # "openai" or "ollama"
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-3.5-turbo", env="OPENAI_MODEL")
    
    # Ollama Configuration
    ollama_host: str = Field("http://localhost:11434", env="OLLAMA_HOST")
    ollama_model: str = Field("deepseek-coder:latest", env="OLLAMA_MODEL")
    
    @property
    def current_ollama_model(self) -> str:
        """Get current Ollama model, checking environment variables first"""
        return os.getenv("OLLAMA_MODEL", self.ollama_model)
    
    # Application Settings
    debug_mode: bool = Field(False, env="DEBUG_MODE")
    log_level: str = Field("info", env="LOG_LEVEL")
    max_tokens: int = Field(2000, env="MAX_TOKENS")
    temperature: float = Field(0.7, env="TEMPERATURE")
    
    # Database Configuration
    database_url: str = Field("sqlite:///nexus.db", env="DATABASE_URL")
    
    # Web Interface Settings
    web_host: str = Field("localhost", env="WEB_HOST")
    web_port: int = Field(8000, env="WEB_PORT")
    
    # Security
    secret_key: str = Field("default-secret-key", env="SECRET_KEY")
    session_timeout: int = Field(3600, env="SESSION_TIMEOUT")
    
    # Rate Limiting
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(60, env="RATE_LIMIT_WINDOW")
    
    # Memory and Context
    conversation_memory_size: int = Field(10, env="CONVERSATION_MEMORY_SIZE")
    context_window_size: int = Field(4000, env="CONTEXT_WINDOW_SIZE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global configuration instance
config = Config()
