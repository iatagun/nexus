"""
Nexus AI Assistant - Main Application Entry Point
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv
from nexus import AIAssistant, setup_logger
from nexus.utils.helpers import check_ollama_status, start_ollama_if_needed, check_interactive_environment

# Load environment variables
load_dotenv()


def main():
    """Main application entry point"""
    
    # Set up logging
    logger = setup_logger()
    
    # Check if we're in an interactive environment
    if not check_interactive_environment():
        print("❌ This application requires an interactive terminal.")
        print("Please run from a command prompt or terminal directly.")
        return 1
    
    # Check Ollama status if using Ollama provider
    import os
    model_provider = os.getenv("MODEL_PROVIDER", "ollama").lower()
    if model_provider == "ollama":
        is_running, error = check_ollama_status()
        if not is_running:
            print(f"⚠️  Ollama issue: {error}")
            if not start_ollama_if_needed():
                print("❌ Cannot start Ollama. Please start it manually:")
                print("   ollama serve")
                return 1
    
    print("🚀 Welcome to Nexus AI Assistant!")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("Type 'reset' to clear conversation history.")
    print("Type 'help' for more commands.")
    print("-" * 50)
    
    try:
        # Initialize the AI assistant
        assistant = AIAssistant()
        print("✅ AI Assistant initialized successfully!")
        print(f"📡 Using {assistant.model_provider} with model: {assistant.model_name}")
        
        while True:
            try:
                # Get user input with better error handling
                try:
                    user_input = input("\n💭 You: ").strip()
                except EOFError:
                    print("\n\n👋 Session ended. Goodbye!")
                    break
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye! Thanks for using Nexus AI Assistant!")
                    break
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye! Thanks for using Nexus AI Assistant!")
                    break
                
                elif user_input.lower() == 'reset':
                    assistant.reset_conversation()
                    print("\n🔄 Conversation history cleared!")
                    continue
                
                elif user_input.lower() == 'help':
                    print("\n📖 Available commands:")
                    print("  - quit/exit/bye: Exit the application")
                    print("  - reset: Clear conversation history")
                    print("  - help: Show this help message")
                    print("  - status: Show current model and provider")
                    continue
                
                elif user_input.lower() == 'status':
                    print(f"\n📊 Status:")
                    print(f"  Provider: {assistant.model_provider}")
                    print(f"  Model: {assistant.model_name}")
                    print(f"  Messages in memory: {len(assistant.memory.messages)}")
                    continue
                
                elif not user_input:
                    print("❌ Please enter a question or command.")
                    continue
                
                # Get response from assistant
                print("\n🤖 Nexus: ", end="", flush=True)
                response = assistant.ask(user_input)
                print(response)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                print(f"\n❌ An error occurred: {e}")
                print("Type 'help' for available commands or 'quit' to exit.")
                continue
                
    except Exception as e:
        logger.error(f"Failed to initialize AI Assistant: {e}")
        print(f"❌ Failed to start Nexus AI Assistant: {e}")
        print("Please check your configuration and try again.")
        print("\nPossible solutions:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check if your model is available: ollama list")
        print("3. Verify your .env configuration")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
