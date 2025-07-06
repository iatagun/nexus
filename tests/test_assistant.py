"""
Tests for Nexus AI Assistant Core Functionality
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from nexus.core.assistant import AIAssistant, ConversationMemory
from nexus.core.config import Config


class TestConversationMemory:
    """Test cases for ConversationMemory class"""
    
    def test_initialization(self):
        """Test memory initialization"""
        memory = ConversationMemory(max_size=5)
        assert memory.max_size == 5
        assert len(memory.messages) == 0
    
    def test_add_message(self):
        """Test adding messages to memory"""
        memory = ConversationMemory(max_size=3)
        
        memory.add_message("user", "Hello")
        assert len(memory.messages) == 1
        assert memory.messages[0]["role"] == "user"
        assert memory.messages[0]["content"] == "Hello"
    
    def test_memory_limit(self):
        """Test memory size limit"""
        memory = ConversationMemory(max_size=2)
        
        memory.add_message("user", "Message 1")
        memory.add_message("assistant", "Response 1")
        memory.add_message("user", "Message 2")
        
        # Should only keep the last 2 messages
        assert len(memory.messages) == 2
        assert memory.messages[0]["content"] == "Response 1"
        assert memory.messages[1]["content"] == "Message 2"
    
    def test_get_context(self):
        """Test getting conversation context"""
        memory = ConversationMemory()
        
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there!")
        
        context = memory.get_context()
        assert len(context) == 2
        assert context[0] == {"role": "user", "content": "Hello"}
        assert context[1] == {"role": "assistant", "content": "Hi there!"}
    
    def test_clear(self):
        """Test clearing memory"""
        memory = ConversationMemory()
        
        memory.add_message("user", "Hello")
        memory.clear()
        
        assert len(memory.messages) == 0


class TestConfig:
    """Test cases for Config class"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = Config()
        
        assert config.openai_model == "gpt-3.5-turbo"
        assert config.debug_mode == False
        assert config.log_level == "info"
        assert config.max_tokens == 2000
        assert config.temperature == 0.7


class TestAIAssistant:
    """Test cases for AIAssistant class"""
    
    @patch('nexus.core.assistant.openai.OpenAI')
    def test_initialization(self, mock_openai):
        """Test assistant initialization"""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        assistant = AIAssistant()
        
        assert assistant.client == mock_client
        assert assistant.memory is not None
        assert len(assistant.memory.messages) == 1  # System prompt
    
    @patch('nexus.core.assistant.openai.OpenAI')
    def test_ask_method(self, mock_openai):
        """Test the ask method"""
        # Mock the OpenAI client and response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        assistant = AIAssistant()
        response = assistant.ask("Test question")
        
        assert response == "Test response"
        assert len(assistant.memory.messages) == 3  # system + user + assistant
    
    @patch('nexus.core.assistant.openai.OpenAI')
    def test_reset_conversation(self, mock_openai):
        """Test conversation reset"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        assistant = AIAssistant()
        assistant.memory.add_message("user", "Hello")
        assistant.memory.add_message("assistant", "Hi!")
        
        assert len(assistant.memory.messages) == 3  # system + user + assistant
        
        assistant.reset_conversation()
        
        assert len(assistant.memory.messages) == 1  # Only system prompt
    
    @patch('nexus.core.assistant.openai.OpenAI')
    def test_chat_alias(self, mock_openai):
        """Test that chat method is an alias for ask"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Chat response"
        
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        assistant = AIAssistant()
        response = assistant.chat("Test message")
        
        assert response == "Chat response"


if __name__ == "__main__":
    pytest.main([__file__])
