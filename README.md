# Nexus - AI Assistant

An intelligent AI assistant designed to help users with various tasks through natural language processing and automated responses.

## 🚀 Features

- **Multiple AI Providers**: Supports both OpenAI API and local Ollama models
- **Natural Language Processing**: Understands and responds to user queries in natural language
- **Task Automation**: Helps automate routine tasks and workflows
- **Intelligent Responses**: Provides contextual and helpful responses
- **User-Friendly Interface**: Easy to use command line and web interfaces
- **Conversation Memory**: Maintains context across conversations
- **Local AI Support**: Run completely offline with Ollama models
- **Extensible Architecture**: Built to support future enhancements and integrations

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- **For OpenAI**: OpenAI API key
- **For Ollama**: Ollama installed and running locally
- Git (for development)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nexus.git
   cd nexus
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**
   ```bash
   # Copy the example configuration file
   copy .env.example .env
   
   # Edit .env file with your preferred settings:
   # For Ollama (local AI):
   MODEL_PROVIDER=ollama
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=deepseek-coder:latest
   
   # For OpenAI:
   MODEL_PROVIDER=openai
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

4. **Install and Start Ollama (if using local AI)**
   ```bash
   # Download from https://ollama.com or use package manager
   # Windows: Download installer
   # macOS: brew install ollama
   # Linux: curl -fsSL https://ollama.com/install.sh | sh
   
   # Start Ollama
   ollama serve
   
   # Pull a model (optional, will auto-download if needed)
   ollama pull deepseek-coder:latest
   ```

## 🎯 Usage

### Quick Start
```bash
# Test your setup
python test_setup.py

# Start interactive chat
python main.py

# Or use the CLI
nexus chat
```

### Command Line Interface

```bash
# Interactive chat mode
nexus chat

# Ask single question
nexus ask "What is artificial intelligence?"

# List available models
nexus models

# Pull new Ollama model
nexus pull llama3.2

# Launch web interface
nexus web
```

### Basic Usage

```python
from nexus import AIAssistant

# Initialize the assistant (uses .env configuration)
assistant = AIAssistant()

# Ask a question
response = assistant.ask("What's the weather like today?")
print(response)

# Chat with memory
response1 = assistant.ask("My name is John")
response2 = assistant.ask("What's my name?")  # Will remember "John"
```

### Model Switching

You can easily switch between providers by updating your `.env` file:

```bash
# Use local Ollama
MODEL_PROVIDER=ollama
OLLAMA_MODEL=deepseek-coder:latest

# Use OpenAI
MODEL_PROVIDER=openai  
OPENAI_MODEL=gpt-4
```

### Advanced Features

- **Custom Commands**: Create custom commands for specific tasks
- **Integration Support**: Connect with external APIs and services
- **Conversation Memory**: Maintains context across conversations
- **Multiple Models**: Switch between different AI models easily
- **Offline Operation**: Works completely offline with Ollama

## 📖 Documentation

For detailed documentation, please visit our [Wiki](https://github.com/yourusername/nexus/wiki) or check the `docs/` directory.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📊 Project Status

- **Version**: 1.0.0
- **Status**: Active Development
- **License**: MIT (see [LICENSE](LICENSE) file)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Model Provider Configuration
MODEL_PROVIDER=ollama  # "openai" or "ollama"

# Ollama Configuration (for local AI)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=deepseek-coder:latest

# OpenAI Configuration (for cloud AI)
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Application Settings
DEBUG_MODE=true
LOG_LEVEL=info
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### Supported Models

**Ollama Models** (Local):
- `deepseek-coder:latest` - Excellent for coding tasks
- `llama3.2:latest` - General purpose conversations
- `gemma3:latest` - Google's Gemma model
- Many more available via `ollama pull <model>`

**OpenAI Models** (Cloud):
- `gpt-3.5-turbo` - Fast and efficient
- `gpt-4` - Most capable model
- `gpt-4-turbo` - Latest optimized version

## 📝 Changelog

### Version 1.0.0
- Initial release
- Basic AI assistant functionality
- Natural language processing capabilities

## 🐛 Known Issues

- None at this time

## 📞 Support

If you encounter any issues or have questions:

- **Issues**: [GitHub Issues](https://github.com/yourusername/nexus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/nexus/discussions)
- **Email**: support@nexus-ai.com

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the open-source community for their valuable tools and libraries

## 🔗 Links

- [Project Homepage](https://nexus-ai.com)
- [Documentation](https://docs.nexus-ai.com)
- [API Reference](https://api.nexus-ai.com)

---

**Made with ❤️ by the Nexus Team**
