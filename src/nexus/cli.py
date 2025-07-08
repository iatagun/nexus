"""
Command Line Interface for Nexus AI Assistant
"""

import argparse
import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv
from nexus import AIAssistant, setup_logger, __version__

# Load environment variables
load_dotenv()


def create_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        prog="nexus",
        description="Nexus AI Assistant - Your intelligent AI companion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nexus chat                    # Start interactive chat mode
  nexus ask "What is Python?"   # Ask a single question
  nexus web                     # Launch web interface
  nexus --version               # Show version information

For more information, visit: https://github.com/yourusername/nexus
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Nexus AI Assistant v{__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Chat command
    chat_parser = subparsers.add_parser(
        "chat",
        help="Start interactive chat mode"
    )
    chat_parser.add_argument(
        "--reset",
        action="store_true",
        help="Start with a fresh conversation"
    )
    chat_parser.add_argument(
        "--model",
        help="Model to use (e.g., deepseek-coder:latest, gemma3:latest)"
    )
    
    # Ask command
    ask_parser = subparsers.add_parser(
        "ask",
        help="Ask a single question"
    )
    ask_parser.add_argument(
        "question",
        help="The question to ask the AI assistant"
    )
    ask_parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Response creativity (0.0-2.0)"
    )
    ask_parser.add_argument(
        "--max-tokens",
        type=int,
        default=2000,
        help="Maximum response length"
    )
    ask_parser.add_argument(
        "--model",
        help="Model to use (e.g., deepseek-coder:latest, gemma3:latest)"
    )
    
    # Web command
    web_parser = subparsers.add_parser(
        "web",
        help="Launch web interface"
    )
    web_parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind the web server"
    )
    web_parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port to bind the web server"
    )
    
    # Models command
    models_parser = subparsers.add_parser(
        "models",
        help="List available models"
    )
    models_parser.add_argument(
        "--provider",
        choices=["ollama", "openai"],
        help="Specify model provider"
    )
    
    # Pull model command
    pull_parser = subparsers.add_parser(
        "pull",
        help="Pull a model from Ollama"
    )
    pull_parser.add_argument(
        "model_name",
        help="Name of the model to pull"
    )
    
    # Learning stats command
    stats_parser = subparsers.add_parser(
        "stats",
        help="Show learning and improvement statistics"
    )
    
    # Feedback command
    feedback_parser = subparsers.add_parser(
        "feedback",
        help="Provide feedback on the last response"
    )
    feedback_parser.add_argument(
        "rating",
        type=int,
        choices=[1, 0, -1],
        help="Feedback rating (1: positive, 0: neutral, -1: negative)"
    )
    
    # Improvement command
    improve_parser = subparsers.add_parser(
        "improve",
        help="Show improvement suggestions and learning status"
    )
    
    return parser


def cmd_chat(args):
    """Handle chat command"""
    print("🚀 Welcome to Nexus AI Assistant!")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("Type 'reset' to clear conversation history.")
    print("Type 'help' for more commands.")
    print("-" * 50)
    
    try:
        # Override model if specified
        if args.model:
            os.environ['OLLAMA_MODEL'] = args.model
            print(f"🤖 Using model: {args.model}")
        
        assistant = AIAssistant()
        
        if args.reset:
            assistant.reset_conversation()
            print("🔄 Started with fresh conversation!")
        
        while True:
            try:
                user_input = input("\n💭 You: ").strip()
                
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
                    print("  - feedback <rating>: Rate last response (1=good, 0=neutral, -1=bad)")
                    print("  - stats: Show learning statistics")
                    print("  - improve: Show improvement suggestions")
                    continue
                
                elif user_input.lower().startswith('feedback '):
                    try:
                        rating = int(user_input.split()[1])
                        if rating in [-1, 0, 1]:
                            # Get last conversation
                            history = assistant.get_conversation_history()
                            if len(history) >= 2:
                                last_user = history[-2]['content']
                                last_assistant = history[-1]['content']
                                result = assistant.provide_feedback(last_user, last_assistant, rating)
                                print(f"\n💡 Feedback recorded! Quality score: {result['overall_quality']:.2f}")
                                if result['suggestions']:
                                    print("🎯 Improvement suggestions:")
                                    for suggestion in result['suggestions']:
                                        print(f"  - {suggestion}")
                            else:
                                print("❌ No recent conversation to rate.")
                        else:
                            print("❌ Rating must be -1, 0, or 1")
                    except (ValueError, IndexError):
                        print("❌ Invalid feedback format. Use: feedback <rating>")
                    continue
                
                elif user_input.lower() == 'stats':
                    stats = assistant.get_learning_stats()
                    print("\n📊 Learning Statistics:")
                    print(f"  Total conversations: {stats['total_conversations']}")
                    print(f"  Positive feedback rate: {stats['positive_feedback_rate']:.1%}")
                    print(f"  Average quality score: {stats['avg_quality_score']:.1%}")
                    print(f"  Learned patterns: {stats['learned_patterns']}")
                    continue
                
                elif user_input.lower() == 'improve':
                    summary = assistant.continuous_improvement_summary()
                    print(f"\n🧠 Continuous Improvement Status:")
                    print(f"  Level: {summary['improvement_level']}")
                    print(f"  Total interactions: {summary['total_interactions']}")
                    print(f"  Satisfaction rate: {summary['satisfaction_rate']}")
                    print(f"  Quality score: {summary['quality_score']}")
                    print(f"  Adaptive capabilities: {', '.join(summary['adaptive_capabilities'])}")
                    continue
                
                elif not user_input:
                    print("❌ Please enter a question or command.")
                    continue
                
                print("\n🤖 Nexus: ", end="", flush=True)
                response = assistant.ask(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using Nexus AI Assistant!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Failed to start Nexus AI Assistant: {e}")
        return 1
    
    return 0


def cmd_ask(args):
    """Handle ask command"""
    try:
        # Override model if specified
        if args.model:
            os.environ['OLLAMA_MODEL'] = args.model
            print(f"🤖 Using model: {args.model}")
        
        assistant = AIAssistant()
        
        print(f"💭 Question: {args.question}")
        print("\n🤖 Nexus: ", end="", flush=True)
        
        response = assistant.ask(
            args.question,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        
        print(response)
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def cmd_web(args):
    """Handle web command"""
    try:
        import streamlit.web.cli as stcli
        import sys
        
        # Get the path to the web app (in root directory, not src)
        web_app_path = Path(__file__).parent.parent.parent / "web_app.py"
        
        if not web_app_path.exists():
            print("❌ Web app file not found at:", web_app_path)
            print("Please make sure web_app.py exists in the project root.")
            return 1
        
        print(f"🌐 Starting Nexus AI Assistant web interface...")
        print(f"🔗 Open your browser to: http://{args.host}:{args.port}")
        
        # Set up Streamlit arguments
        sys.argv = [
            "streamlit",
            "run",
            str(web_app_path),
            "--server.address", args.host,
            "--server.port", str(args.port),
            "--server.headless", "true"
        ]
        
        # Run Streamlit
        stcli.main()
        
    except ImportError:
        print("❌ Streamlit is not installed. Install it with:")
        print("   pip install streamlit")
        return 1
    except Exception as e:
        print(f"❌ Failed to start web interface: {e}")
        return 1


def cmd_models(args):
    """Handle models command"""
    try:
        if args.provider == "ollama" or (not args.provider and os.getenv("MODEL_PROVIDER", "ollama") == "ollama"):
            import ollama
            from nexus.core.config import config
            
            client = ollama.Client(host=config.ollama_host)
            models = client.list()
            
            print("Available Ollama models:")
            print("-" * 30)
            if models.models:
                for model in models.models:
                    name = model.model
                    size = model.size
                    size_mb = size / (1024 * 1024) if size else 0
                    modified = model.modified_at.strftime("%Y-%m-%d %H:%M") if model.modified_at else "Unknown"
                    print(f"• {name}")
                    print(f"  Size: {size_mb:.1f} MB")
                    print(f"  Modified: {modified}")
                    print()
            else:
                print("No models found")
            
        elif args.provider == "openai":
            print("OpenAI models list requires API access")
            print("Common models: gpt-3.5-turbo, gpt-4, gpt-4-turbo")
            
        return 0
        
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return 1


def cmd_pull(args):
    """Handle pull command"""
    try:
        import ollama
        from nexus.core.config import config
        
        print(f"Pulling model: {args.model_name}")
        client = ollama.Client(host=config.ollama_host)
        
        # Pull the model with progress
        for progress in client.pull(args.model_name, stream=True):
            if 'status' in progress:
                print(f"Status: {progress['status']}")
            if 'completed' in progress and 'total' in progress:
                percent = (progress['completed'] / progress['total']) * 100
                print(f"Progress: {percent:.1f}%")
        
        print(f"✅ Successfully pulled model: {args.model_name}")
        return 0
        
    except Exception as e:
        print(f"❌ Error pulling model: {e}")
        return 1


def cmd_stats(args):
    """Handle stats command"""
    try:
        assistant = AIAssistant()
        stats = assistant.get_learning_stats()
        
        print("📊 Nexus Learning Statistics")
        print("=" * 40)
        print(f"Total conversations: {stats['total_conversations']}")
        print(f"Positive feedback rate: {stats['positive_feedback_rate']:.1%}")
        print(f"Average quality score: {stats['avg_quality_score']:.1%}")
        print(f"Average response time: {stats['avg_response_time']:.2f}s")
        
        print("\n🧠 Learned Patterns:")
        for pattern_type, count in stats['learned_patterns'].items():
            print(f"  {pattern_type}: {count} patterns")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        return 1


def cmd_feedback(args):
    """Handle feedback command"""
    try:
        print("💡 Feedback feature requires an active conversation.")
        print("Use this command within the chat interface:")
        print("  nexus chat")
        print("  > your question")
        print("  > feedback 1  # Rate the response")
        return 0
        
    except Exception as e:
        print(f"❌ Error with feedback: {e}")
        return 1


def cmd_improve(args):
    """Handle improve command"""
    try:
        assistant = AIAssistant()
        summary = assistant.continuous_improvement_summary()
        
        print("🧠 Continuous Improvement Status")
        print("=" * 40)
        print(f"Improvement Level: {summary['improvement_level']}")
        print(f"Total Interactions: {summary['total_interactions']}")
        print(f"Satisfaction Rate: {summary['satisfaction_rate']}")
        print(f"Quality Score: {summary['quality_score']}")
        
        print("\n🎯 Adaptive Capabilities:")
        for capability in summary['adaptive_capabilities']:
            print(f"  ✓ {capability}")
        
        print("\n💡 Suggestions:")
        suggestions = assistant.suggest_improvements()
        for suggestion in suggestions:
            print(f"  • {suggestion}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error getting improvement info: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logger()
    
    if not args.command:
        # Default to chat mode if no command specified
        args.command = "chat"
        args.reset = False
    
    # Route to appropriate command handler
    if args.command == "chat":
        return cmd_chat(args)
    elif args.command == "ask":
        return cmd_ask(args)
    elif args.command == "web":
        return cmd_web(args)
    elif args.command == "models":
        return cmd_models(args)
    elif args.command == "pull":
        return cmd_pull(args)
    elif args.command == "stats":
        return cmd_stats(args)
    elif args.command == "feedback":
        return cmd_feedback(args)
    elif args.command == "improve":
        return cmd_improve(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
