# OpenHands Swarm Controller Specifications

## Project Overview
The OpenHands Swarm Controller is a GUI-based management system for orchestrating OpenHands agent swarms. It provides:

- LiteLLM configuration management
- OpenHands endpoint configuration
- Multi-language support (i18n) with UTF-8 encoding
- Visual swarm monitoring and control
- Integrated task scheduling

## Key Features
1. **OpenHands Integration**:
   - URL configuration for OpenHands endpoints
   - Real-time swarm status monitoring
   - Task queue visualization

2. **LiteLLM Configuration**:
   - Model selection interface
   - API key management
   - Prompt template configuration

3. **Internationalization**:
   - UTF-8 encoded localization
   - Language selection UI
   - Dynamic text resizing

4. **GUI Components**:
   - Dashboard with swarm metrics
   - Configuration panels for all components
   - Real-time logging display

## Technical Specifications
- **Encoding**: UTF-8
- **Localization**: gettext-based i18n
- **GUI Framework**: PySide6 (Qt for Python)
- **Configuration Storage**: JSON with schema validation
- **Network Protocol**: WebSocket for real-time updates

## Configuration Structure
```json
{
  "openhands": {
    "endpoint": "ws://localhost:51090",
    "api_key": "",
    "timeout": 30
  },
  "litellm": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "ui": {
    "language": "en_US",
    "theme": "dark",
    "font_size": 12
  }
}
```

## Roadmap
1. Implement core GUI framework
2. Add OpenHands connection management
3. Develop LiteLLM configuration interface
4. Implement i18n localization system
5. Create configuration validation system