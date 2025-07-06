"""
Core AI Assistant implementation for Nexus
"""

import openai
import ollama
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..core.config import config
from ..utils.logger import nexus_logger


class ConversationMemory:
    """Manages conversation history and context"""
    
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.messages: List[Dict[str, str]] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        
        # Keep only the last max_size messages
        if len(self.messages) > self.max_size:
            self.messages = self.messages[-self.max_size:]
    
    def get_context(self) -> List[Dict[str, str]]:
        """Get conversation context for OpenAI API"""
        return [{"role": msg["role"], "content": msg["content"]} 
                for msg in self.messages]
    
    def clear(self):
        """Clear conversation history"""
        self.messages.clear()


class AIAssistant:
    """
    Main AI Assistant class that handles natural language interactions
    """
    
    def __init__(self):
        """Initialize the AI Assistant"""
        self.memory = ConversationMemory(config.conversation_memory_size)
        self.logger = nexus_logger
        self.model_provider = config.model_provider.lower()
        
        # Initialize the appropriate client based on provider
        if self.model_provider == "openai":
            if not config.openai_api_key:
                raise ValueError("OpenAI API key is required when using OpenAI provider")
            self.client = openai.OpenAI(api_key=config.openai_api_key)
            self.model_name = config.openai_model
        elif self.model_provider == "ollama":
            self.client = ollama.Client(host=config.ollama_host)
            self.model_name = config.ollama_model
            # Test Ollama connection
            try:
                models = self.client.list()
                available_models = [model.model for model in models.models]
                if self.model_name not in available_models:
                    self.logger.warning(f"Model {self.model_name} not found. Available models: {available_models}")
                    if available_models:
                        self.model_name = available_models[0]
                        self.logger.info(f"Using available model: {self.model_name}")
            except Exception as e:
                self.logger.error(f"Failed to connect to Ollama: {e}")
                raise ConnectionError(f"Cannot connect to Ollama at {config.ollama_host}")
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
        
        # System prompt for the assistant
        self.system_prompt = """
        You are Nexus, an intelligent AI assistant designed to help users with various tasks.
        You are helpful, accurate, and provide clear explanations.
        You can assist with:
        - Answering questions and providing information
        - Helping with coding and technical problems
        - Automating tasks and workflows
        - Providing creative solutions
        
        Always be polite, professional, and helpful in your responses.
        """
        
        self.memory.add_message("system", self.system_prompt)
        self.logger.info(f"AI Assistant initialized successfully with {self.model_provider} provider")
        self.logger.info(f"Using model: {self.model_name}")
    
    def ask(self, question: str, **kwargs) -> str:
        """
        Ask a question to the AI assistant
        
        Args:
            question: The user's question or prompt
            **kwargs: Additional parameters for the API
            
        Returns:
            The assistant's response
        """
        try:
            self.logger.info(f"Processing question: {question[:100]}...")
            
            # Add user message to memory
            self.memory.add_message("user", question)
            
            # Prepare messages for API call
            messages = self.memory.get_context()
            
            # Make API call based on provider
            if self.model_provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    max_tokens=kwargs.get("max_tokens", config.max_tokens),
                    temperature=kwargs.get("temperature", config.temperature),
                    **kwargs
                )
                assistant_response = response.choices[0].message.content
                
            elif self.model_provider == "ollama":
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                    options={
                        'temperature': kwargs.get("temperature", config.temperature),
                        'num_predict': kwargs.get("max_tokens", config.max_tokens),
                    }
                )
                assistant_response = response['message']['content']
            
            # Add assistant response to memory
            self.memory.add_message("assistant", assistant_response)
            
            self.logger.info("Question processed successfully")
            return assistant_response
            
        except Exception as e:
            error_msg = f"Error processing question: {str(e)}"
            self.logger.error(error_msg)
            return f"Sorry, I encountered an error: {str(e)}"
    
    def chat(self, message: str) -> str:
        """
        Alias for ask method for more conversational interface
        
        Args:
            message: The user's message
            
        Returns:
            The assistant's response
        """
        return self.ask(message)
    
    def reset_conversation(self):
        """Reset the conversation memory"""
        self.memory.clear()
        self.memory.add_message("system", self.system_prompt)
        self.logger.info("Conversation reset")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history"""
        return self.memory.messages.copy()
    
    def set_system_prompt(self, prompt: str):
        """
        Set a custom system prompt
        
        Args:
            prompt: The new system prompt
        """
        self.system_prompt = prompt
        self.reset_conversation()
        self.logger.info("System prompt updated")
    
    async def ask_async(self, question: str, **kwargs) -> str:
        """
        Async version of ask method
        
        Args:
            question: The user's question or prompt
            **kwargs: Additional parameters for the OpenAI API
            
        Returns:
            The assistant's response
        """
        # For now, just call the sync version
        # In a real implementation, you'd use an async OpenAI client
        return self.ask(question, **kwargs)
