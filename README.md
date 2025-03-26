# OpenHands Swarm Controller

![Project Status](https://img.shields.io/badge/status-canceled-red)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Encoding](https://img.shields.io/badge/encoding-UTF--8-green)

The OpenHands Swarm Controller is a comprehensive GUI application for managing and orchestrating OpenHands agent swarms. It provides:

- 🖥️ Intuitive GUI for swarm management
- 🔗 OpenHands endpoint configuration
- 🤖 LiteLLM integration with visual configuration
- 🌍 Multi-language support (i18n)
- 📊 Real-time monitoring and analytics

## Features

### OpenHands Integration
- Configure multiple OpenHands endpoints
- Visualize swarm status and health
- Manage task queues and execution

### LiteLLM Configuration
- Model selection and parameter tuning
- API key management
- Prompt template editor

### Internationalization
- UTF-8 encoded localization
- Language selection UI
- Dynamic text resizing

### Configuration Management
- JSON-based configuration storage
- Schema validation
- Import/export functionality

## Getting Started

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python src/main.py
```

### Configuration
Edit `config/config.json` to set up your OpenHands endpoints and LiteLLM parameters.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
