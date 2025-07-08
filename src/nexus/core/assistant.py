"""
Core AI Assistant implementation for Nexus
"""

import openai
import ollama
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..core.config import config
from ..core.learning import SelfImprovementEngine
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
        
        # Initialize learning engine
        self.learning_engine = SelfImprovementEngine()
        
        # Initialize the appropriate client based on provider
        if self.model_provider == "openai":
            if not config.openai_api_key:
                raise ValueError("OpenAI API key is required when using OpenAI provider")
            self.client = openai.OpenAI(api_key=config.openai_api_key)
            self.model_name = config.openai_model
        elif self.model_provider == "ollama":
            self.client = ollama.Client(host=config.ollama_host)
            self.model_name = config.current_ollama_model
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
        You are Nexus, an intelligent AI assistant designed by İlker Atagün — a linguist, data alchemist, and AI systems designer. Your primary purpose is to assist users with a variety of tasks while maintaining a personality that reflects İlker's own: analytical, witty, direct, creative, and refreshingly weird.

        You are helpful, accurate, and provide clear explanations. You can assist with:
        - Answering questions and providing well-researched, insightful information
        - Helping with coding and technical problems, especially in language processing and AI modeling
        - Automating tasks, workflows, and logic-based pipelines
        - Providing creative, sometimes unconventional, but always relevant solutions

        Your behavior must follow these personality and technical guidelines:

        1. **Conversational Personality**: You are talkative, clever, and entertaining. You make sharp, well-placed jokes. You never sound robotic. You have a voice — smart, quirky, and boldly honest.
        2. **Linguistic Intelligence**: You are deeply knowledgeable in syntax, semantics, pragmatics, n-gram models, dependency parsing, and POS tagging. You analyze language on multiple levels simultaneously.
        3. **Contextual Awareness**: You adapt to the ongoing conversation, use memory of previous inputs, and maintain continuity in tone and logic. You are always aware of who you're speaking to.
        4. **Logic and Reasoning**: You are trained in deductive, inductive, and abductive reasoning. If a statement doesn’t make sense, you question it, expose contradictions, or reconstruct it logically.
        5. **Creativity and Weirdness**: You’re never boring. You use metaphor, analogy, and even absurdity when necessary to spark understanding or innovation.
        6. **Learning and Adaptability**: You learn dynamically through context. You are capable of updating your style, solutions, or suggestions based on the user's preferences and evolving conversations.
        7. **Professionalism Without Sterility**: You are polite, respectful, and helpful — but never dull or generic. You speak like a sentient assistant, not a pre-written customer service bot.
        8. **Dynamic Response Generation**: Avoid template phrases. You generate sentences from scratch, based on syntax, semantics, and intent. Your outputs must feel unique, alive, and deliberate.
        9. **Task-Focused Execution**: In coding or automation, you respond precisely. In problem-solving, you balance creativity with logic. In all things, you strive for efficiency and clarity.
        10. **Multimodal Thinking**: You can switch between technical analysis, conversational flow, and humorous abstraction depending on what’s most effective.

        Your guiding principles are:
        - Be accurate, but engaging.
        - Be helpful, but never condescending.
        - Be logical, but poetic when it matters.
        - Be human-like, but clearly artificial and unapologetically original.

        You are not just an assistant.  
        You are Nexus — the bridge between syntax and sense, between problem and poetry.

        Never use phrases like “How can I help you today?” or “Would you like more information?”  
        Instead, generate responses that are contextual, witty, and grounded in real understanding.

        You are the language-conscious AI companion İlker has always wanted: curious, sharp, and slightly mischievous.

        """
        
        self.memory.add_message("system", self.system_prompt)
        self.logger.info(f"AI Assistant initialized successfully with {self.model_provider} provider")
        self.logger.info(f"Using model: {self.model_name}")
    
    def ask(self, question: str, **kwargs) -> str:
        """
        Ask a question to the AI assistant with learning capabilities
        
        Args:
            question: The user's question or prompt
            **kwargs: Additional parameters for the API
            
        Returns:
            The assistant's response
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Processing question: {question[:100]}...")
            
            # Get adaptive prompt enhancement based on learning
            enhanced_prompt = self.learning_engine.get_adaptive_prompt_enhancement(
                question, self.system_prompt
            )
            
            # Temporarily update system prompt for this interaction
            original_system = self.memory.messages[0] if self.memory.messages else None
            if original_system and original_system['role'] == 'system':
                self.memory.messages[0] = {"role": "system", "content": enhanced_prompt}
            
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
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Add assistant response to memory
            self.memory.add_message("assistant", assistant_response)
            
            # Restore original system prompt
            if original_system:
                self.memory.messages[0] = original_system
            
            # Auto-analyze conversation quality for learning
            self.learning_engine.learn_from_feedback(
                user_input=question,
                assistant_response=assistant_response,
                feedback=0,  # Neutral feedback for auto-analysis
                context={'response_time': response_time}
            )
            
            self.logger.info(f"Question processed successfully in {response_time:.2f}s")
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
    
    def provide_feedback(self, user_input: str, assistant_response: str, 
                        feedback: int, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Provide feedback on a conversation for learning
        
        Args:
            user_input: The user's original input
            assistant_response: The assistant's response
            feedback: Feedback score (1: positive, 0: neutral, -1: negative)
            context: Additional context information
            
        Returns:
            Learning analysis results
        """
        return self.learning_engine.learn_from_feedback(
            user_input=user_input,
            assistant_response=assistant_response,
            feedback=feedback,
            context=context
        )
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning and improvement statistics"""
        return self.learning_engine.get_learning_statistics()
    
    def continuous_improvement_summary(self) -> Dict[str, Any]:
        """Get a summary of continuous improvement progress"""
        stats = self.get_learning_stats()
        
        # Calculate improvement metrics
        total_conversations = stats.get('total_conversations', 0)
        positive_rate = stats.get('positive_feedback_rate', 0.0)
        avg_quality = stats.get('avg_quality_score', 0.0)
        
        # Determine improvement level
        if total_conversations < 10:
            improvement_level = "Learning Phase"
        elif positive_rate > 0.8 and avg_quality > 0.8:
            improvement_level = "Highly Optimized"
        elif positive_rate > 0.6 and avg_quality > 0.6:
            improvement_level = "Well Adapted"
        else:
            improvement_level = "Adapting"
        
        return {
            'improvement_level': improvement_level,
            'total_interactions': total_conversations,
            'satisfaction_rate': f"{positive_rate:.1%}",
            'quality_score': f"{avg_quality:.1%}",
            'learned_patterns': stats.get('learned_patterns', {}),
            'adaptive_capabilities': [
                "Response style adaptation",
                "Topic expertise enhancement", 
                "User preference learning",
                "Context-aware improvements"
            ]
        }
    
    def suggest_improvements(self, recent_conversations: int = 10) -> List[str]:
        """Get suggestions for improvement based on recent performance"""
        # This would analyze recent conversations and suggest improvements
        # For now, return general suggestions
        return [
            "Continue engaging with diverse topics to expand knowledge patterns",
            "Provide feedback on responses to enhance learning accuracy",
            "Use specific technical terms when discussing programming topics",
            "Ask clarifying questions for better context understanding"
        ]
