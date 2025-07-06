# Nexus AI Assistant - Development Guide

## Development Setup

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/nexus.git
cd nexus

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -e ".[dev,all]"
```

### 2. Environment Configuration
```bash
# Copy example environment file
copy .env.example .env

# Edit .env with your API keys
# Required: OPENAI_API_KEY
```

### 3. Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files (optional)
pre-commit run --all-files
```

## Development Workflow

### Code Formatting
```bash
# Format code with Black
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Linting
```bash
# Run flake8
flake8 src/ tests/

# Run mypy for type checking
mypy src/
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nexus

# Run specific test file
pytest tests/test_assistant.py

# Run with verbose output
pytest -v
```

### Running the Application

#### Command Line Interface
```bash
# Interactive chat mode
python main.py
# or
nexus chat

# Ask single question
nexus ask "What is artificial intelligence?"

# Web interface
nexus web
```

#### Web Interface
```bash
# Using Streamlit directly
streamlit run web_app.py

# Using the CLI
nexus web --port 8501
```

### Project Structure
```
nexus/
├── src/nexus/              # Main package
│   ├── core/               # Core functionality
│   │   ├── assistant.py    # AI Assistant class
│   │   └── config.py       # Configuration
│   ├── utils/              # Utilities
│   │   └── logger.py       # Logging setup
│   └── cli.py              # Command line interface
├── tests/                  # Test files
├── docs/                   # Documentation
├── main.py                 # Main application entry
├── web_app.py              # Streamlit web interface
├── requirements.txt        # Dependencies
├── pyproject.toml          # Project configuration
└── README.md               # Project documentation
```

## Adding New Features

### 1. Core Functionality
- Add new methods to `AIAssistant` class in `src/nexus/core/assistant.py`
- Update configuration in `src/nexus/core/config.py` if needed
- Add corresponding tests in `tests/`

### 2. CLI Commands
- Add new command parsers in `src/nexus/cli.py`
- Implement command handler functions
- Update help text and documentation

### 3. Web Interface
- Add new features to `web_app.py`
- Use Streamlit components for UI
- Test in browser

## Code Standards

### Python Style
- Follow PEP 8 style guide
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints for all functions

### Documentation
- Write docstrings for all classes and functions
- Use Google-style docstrings
- Keep README.md updated

### Testing
- Write tests for all new functionality
- Aim for >80% code coverage
- Use pytest fixtures for common test setup

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Install package in development mode: `pip install -e .`

2. **API Key Issues**
   - Check `.env` file exists and contains `OPENAI_API_KEY`
   - Verify API key is valid

3. **Web Interface Issues**
   - Install Streamlit: `pip install streamlit`
   - Check port is not in use
   - Clear Streamlit cache: `streamlit cache clear`

### Getting Help
- Check existing GitHub Issues
- Create new issue with detailed description
- Include error messages and environment details
