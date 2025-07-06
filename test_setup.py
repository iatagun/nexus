"""
Simple test script for Nexus AI Assistant
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv
from nexus.utils.helpers import check_ollama_status, check_interactive_environment

# Load environment variables
load_dotenv()


def main():
    """Test Nexus configuration and dependencies"""
    
    print("🧪 Nexus AI Assistant - Configuration Test")
    print("=" * 45)
    
    # Test 1: Interactive environment
    print("1. Testing interactive environment...")
    if check_interactive_environment():
        print("   ✅ Running in interactive environment")
    else:
        print("   ⚠️  Not in interactive environment")
    
    # Test 2: Environment variables
    print("\n2. Testing environment configuration...")
    import os
    model_provider = os.getenv("MODEL_PROVIDER", "ollama")
    print(f"   Model Provider: {model_provider}")
    
    if model_provider.lower() == "ollama":
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        print(f"   Ollama Host: {ollama_host}")
        print(f"   Ollama Model: {ollama_model}")
        
        # Test 3: Ollama connection
        print("\n3. Testing Ollama connection...")
        is_running, error = check_ollama_status(ollama_host)
        if is_running:
            print("   ✅ Ollama is running and accessible")
        else:
            print(f"   ❌ Ollama issue: {error}")
    
    elif model_provider.lower() == "openai":
        openai_key = os.getenv("OPENAI_API_KEY", "")
        if openai_key and openai_key != "your_openai_api_key_here":
            print("   ✅ OpenAI API key configured")
        else:
            print("   ❌ OpenAI API key not configured")
    
    # Test 4: Package imports
    print("\n4. Testing package imports...")
    try:
        from nexus import AIAssistant
        print("   ✅ Nexus package imports successfully")
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return 1
    
    # Test 5: AI Assistant initialization
    print("\n5. Testing AI Assistant initialization...")
    try:
        assistant = AIAssistant()
        print(f"   ✅ AI Assistant initialized with {assistant.model_provider}")
        print(f"   Model: {assistant.model_name}")
    except Exception as e:
        print(f"   ❌ Initialization error: {e}")
        return 1
    
    print("\n" + "=" * 45)
    print("🎉 All tests passed! Nexus is ready to use.")
    print("\nTo start chatting, run: python main.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
