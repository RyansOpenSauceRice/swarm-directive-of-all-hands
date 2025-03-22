import litellm
import re
from typing import Dict, Any
from pathlib import Path
import json
from urllib.parse import urlparse
from loguru import logger
from prometheus_client import start_http_server, Counter, Gauge
from .config_manager import ConfigManager

# Prometheus metrics
LLM_REQUESTS_TOTAL = Counter('llm_requests_total', 'Total LLM requests', ['model'])
LLM_REQUEST_DURATION = Gauge('llm_request_duration_seconds', 'LLM request duration in seconds', ['model'])
LLM_ERRORS_TOTAL = Counter('llm_errors_total', 'Total LLM errors', ['model'])
LLM_COST_TOTAL = Counter('llm_cost_total', 'Total LLM cost in USD', ['model'])
LLM_TOKENS_TOTAL = Counter('llm_tokens_total', 'Total tokens processed', ['model'])

class LiteLLMManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        # Configure logging
        logger.add("logs/litellm.log", rotation="100 MB", retention="10 days")
        
        # Configure Prometheus if enabled
        prometheus_config = self.config.get('monitoring.prometheus', {})
        if prometheus_config.get('enabled', True):
            try:
                port = prometheus_config.get('port', 8000)
                start_http_server(port)
                logger.info(f"Prometheus metrics server started on port {port}")
            except Exception as e:
                logger.error(f"Failed to start Prometheus server: {str(e)}")
        
        self._setup_litellm()
        
    def _setup_litellm(self):
        """Initialize LiteLLM with configuration settings"""
        litellm.drop_params = True
        litellm.set_verbose = True
        
        # Configure models from config
        for model in self.config.get('litellm.models', []):
            self.register_model(model)
            
    
        
    def _validate_api_key(self, api_key: str) -> bool:
        """Validate API key format"""
        if not api_key:
            return False
        # Check for OpenAI-style API key format
        return bool(re.match(r'^sk-[a-zA-Z0-9]{32,}$', api_key))

    def _validate_url(self, url: str) -> bool:
        """Validate API base URL"""
        if not url:
            return True  # Empty URL is valid (will use default)
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme in ('http', 'https'), result.netloc])
        except:
            return False

    def register_model(self, model_config: Dict[str, Any]):
        """Register a new model with LiteLLM"""
        model_name = model_config['name']
        
        # Validate API key
        api_key = model_config.get('api_key', '')
        if not self._validate_api_key(api_key):
            LLM_ERRORS_TOTAL.labels(model=model_name).inc()
            logger.error(f"Invalid API key format for model {model_name}")
            raise ValueError("Invalid API key format")

        # Validate base URL
        base_url = model_config.get('provider_options', {}).get('api_base', '')
        if not self._validate_url(base_url):
            LLM_ERRORS_TOTAL.labels(model=model_name).inc()
            logger.error(f"Invalid API base URL for model {model_name}: {base_url}")
            raise ValueError("Invalid API base URL")

        # Enable LiteLLM's built-in cost tracking
        config = {
            'model': model_name,
            'api_key': api_key,
            'temperature': model_config.get('temperature', 0.7),
            'max_tokens': model_config.get('max_tokens', 4096),
            'timeout': model_config.get('timeout', 30),
            'retry': {
                'attempts': model_config.get('retry', {}).get('count', 3),
                'delay': model_config.get('retry', {}).get('delay', 2)
            },
            'rate_limit': model_config.get('rate_limit', 60),
            'track_cost': True,  # Enable LiteLLM's built-in cost tracking
            'provider_options': {
                'api_base': base_url,
                'timeout': model_config.get('timeout', 30)
            }
        }
        
        try:
            litellm.register_model(model_name, config)
            logger.info(f"Successfully registered model: {model_name}")
            LLM_REQUESTS_TOTAL.labels(model=model_name).inc()
            
            # Initialize cost tracking
            LLM_COST_TOTAL.labels(model=model_name).inc(0)
            LLM_TOKENS_TOTAL.labels(model=model_name).inc(0)
        except Exception as e:
            LLM_ERRORS_TOTAL.labels(model=model_name).inc()
            logger.error(f"Failed to register model {model_name}: {str(e)}")
            raise

    def get_cost_data(self, model_name: str) -> Dict[str, float]:
        """Get cost data for a specific model"""
        try:
            from litellm import get_cost_data
            return get_cost_data(model=model_name)
        except Exception as e:
            logger.error(f"Failed to get cost data for {model_name}: {str(e)}")
            return {}

    def get_available_models(self) -> list[str]:
        """Get list of available models"""
        return [model['name'] for model in self.config.get('litellm.models', [])]
        
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        for model in self.config.get('litellm.models', []):
            if model['name'] == model_name:
                return model
        return {}
        
    def update_model_config(self, model_name: str, config: Dict[str, Any]):
        """Update configuration for a specific model"""
        models = self.config.get('litellm.models', [])
        for i, model in enumerate(models):
            if model['name'] == model_name:
                models[i] = {**model, **config}
                break
        else:
            models.append(config)
            
        self.config.set('litellm.models', models)
        self.register_model(config)
        
    def remove_model(self, model_name: str):
        """Remove a model configuration"""
        models = self.config.get('litellm.models', [])
        models = [m for m in models if m['name'] != model_name]
        self.config.set('litellm.models', models)
        
    def set_default_model(self, model_name: str):
        """Set the default model for LiteLLM"""
        if model_name in self.get_available_models():
            self.config.set('litellm.default_model', model_name)
            
    def get_default_model(self) -> str:
        """Get the current default model"""
        return self.config.get('litellm.default_model', '')