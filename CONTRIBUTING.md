# Contributing to Nexus AI Assistant

We love your input! We want to make contributing to Nexus AI Assistant as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. **Fork the repo** and create your branch from `main`.
2. **Add tests** if you've added code that should be tested.
3. **Update documentation** if you've changed APIs.
4. **Ensure the test suite passes**.
5. **Make sure your code lints**.
6. **Issue that pull request**!

### Development Setup

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup instructions.

## Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **flake8** for linting
- **mypy** for type checking
- **pytest** for testing

Run these tools before submitting:

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
pytest
```

## Any Contributions You Make Will Be Under the MIT Software License

When you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report Bugs Using GitHub Issues

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/nexus/issues).

### Write Bug Reports With Detail

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** in detail
3. **Explain why it would be useful**
4. **Consider implementation** - how might it work?

## Coding Guidelines

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for function signatures
- Write docstrings for all public functions/classes
- Keep functions focused and small
- Use meaningful variable names

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update DEVELOPMENT.md for development changes
- Include examples in docstrings when helpful

### Testing

- Write tests for new functionality
- Ensure existing tests still pass
- Aim for good test coverage
- Use meaningful test names
- Test both happy path and edge cases

### Git Commit Messages

Write clear, meaningful commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add conversation memory to AI assistant

- Implement ConversationMemory class
- Add memory management to AIAssistant
- Include tests for memory functionality
- Update documentation

Fixes #123
```

## Code Review Process

The core team looks at Pull Requests on a regular basis. After feedback has been given we expect responses within two weeks. After two weeks we may close the pull request if it isn't showing any activity.

## Community

- Be respectful and inclusive
- Help newcomers
- Share knowledge
- Give constructive feedback

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks for major features

Thank you for contributing to Nexus AI Assistant! 🚀
