# Contributing to Swarm Directive

We welcome contributions from the community! Here's how you can help:

## Getting Started
1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature/bugfix
4. Make your changes
5. Submit a pull request

## Development Environment
- Python 3.10+
- OpenHands runtime
- LiteLLM installed
- Playwright for browser automation

## Build System
- Flatpak builds are handled automatically via GitHub Actions
- Failed builds generate logs in `.build-logs/`
- Logs are automatically cleaned up after 3 days
- Check the Actions tab for build results

## Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep functions small and focused
- Write comprehensive docstrings

## Testing
- Write unit tests for new features
- Ensure existing tests pass
- Use pytest for test automation

## Documentation
- Update relevant markdown files
- Add docstrings to new functions/classes
- Keep the SPECIFICATIONS.md file current

## Pull Requests
- Include a clear description of changes
- Reference related issues
- Ensure all tests pass
- Update documentation as needed

## Reporting Issues
- Check existing issues first
- Provide detailed reproduction steps
- Include relevant logs or screenshots
- Specify your environment details