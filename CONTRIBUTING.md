# Contributing to PlayStation Store Tracker

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How to Contribute

### Reporting Bugs

- Use the GitHub issue tracker to report bugs
- Check if the bug has already been reported
- Provide a clear title and description
- Include:
  - Steps to reproduce the issue
  - Expected vs actual behavior
  - Your environment (Python version, OS, etc.)
  - Relevant logs or screenshots

### Feature Requests

- Use the GitHub issue tracker with a "enhancement" label
- Describe the use case and benefits
- Provide examples of how the feature would work

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure code quality:
   - Run tests: `pytest`
   - Add docstrings and type hints for new functions
6. Commit with clear messages (`git commit -m 'Add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request with a clear description

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ps_store_tracker.git
cd ps_store_tracker

# Install dependencies
pip install -e .
pip install pytest

# Copy and configure environment
cp .env.example .env
# Edit .env with your Gmail app password
```

## Code Style

- Follow PEP 8 conventions
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Include type hints in function signatures
- Keep functions focused and modular

## Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for reasonable code coverage

```bash
pytest
```

## Git Commit Messages

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", "Remove", etc.
- Keep the first line under 50 characters
- Link to related issues: "Fixes #123"

## Questions?

Feel free to open an issue for questions or discussion.

Thank you for contributing!
