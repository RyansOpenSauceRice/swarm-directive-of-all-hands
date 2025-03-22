import json
from pathlib import Path
from typing import Any, Optional

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._create_default_config()
            
    def _create_default_config(self) -> dict:
        default_config = {
            "openhands": {
                "endpoints": [],
                "default_timeout": 30,
                "max_retries": 3
            },
            "litellm": {
                "models": [],
                "default_model": "",
                "max_concurrent_requests": 5
            },
            "ui": {
                "language": "en_US",
                "theme": "dark",
                "font_size": 12
            },
            "i18n": {
                "available_languages": ["en_US"],
                "default_language": "en_US",
                "encoding": "UTF-8"
            }
        }
        
        # Save default config
        self.save_config(default_config)
        return default_config
        
    def save_config(self, config: Optional[dict] = None):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config or self.config, f, indent=4)
            
    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key_path: str, value: Any):
        keys = key_path.split('.')
        current = self.config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
        self.save_config()