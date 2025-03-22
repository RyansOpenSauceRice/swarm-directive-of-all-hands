from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QMessageBox, QSpinBox, QDoubleSpinBox,
    QCheckBox, QGroupBox
)
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.litellm_manager import LiteLLMManager

class LiteLLMConfigDialog(QDialog):
    def __init__(self, litellm_manager: 'LiteLLMManager', parent=None):
        super().__init__(parent)
        self.litellm_manager = litellm_manager
        self._setup_ui()
        self._load_current_config()
        
    def _setup_ui(self):
        self.setWindowTitle("LiteLLM Configuration")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Model configuration group
        model_group = QGroupBox("Model Configuration")
        model_layout = QFormLayout()
        
        # Model selection
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.litellm_manager.get_available_models())
        self.model_combo.currentTextChanged.connect(self._load_current_config)
        model_layout.addRow("Model:", self.model_combo)
        
        # API Key
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter API key...")
        model_layout.addRow("API Key:", self.api_key_input)
        
        # Base URL
        self.base_url_input = QLineEdit()
        self.base_url_input.setPlaceholderText("https://api.openai.com/v1")
        model_layout.addRow("API Base URL:", self.base_url_input)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Advanced settings group
        advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QFormLayout()
        
        # Temperature
        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(0, 2)
        self.temperature_input.setSingleStep(0.1)
        self.temperature_input.setValue(0.7)
        advanced_layout.addRow("Temperature:", self.temperature_input)
        
        # Max tokens
        self.max_tokens_input = QSpinBox()
        self.max_tokens_input.setRange(1, 100000)
        self.max_tokens_input.setValue(4096)
        advanced_layout.addRow("Max Tokens:", self.max_tokens_input)
        
        # Timeout
        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(1, 600)
        self.timeout_input.setValue(30)
        self.timeout_input.setSuffix("s")
        advanced_layout.addRow("Timeout:", self.timeout_input)
        
        # Enable caching
        self.cache_checkbox = QCheckBox("Enable response caching")
        advanced_layout.addRow(self.cache_checkbox)
        
        # Retry settings
        self.retry_count_input = QSpinBox()
        self.retry_count_input.setRange(0, 10)
        self.retry_count_input.setValue(3)
        advanced_layout.addRow("Max Retries:", self.retry_count_input)
        
        self.retry_delay_input = QSpinBox()
        self.retry_delay_input.setRange(0, 60)
        self.retry_delay_input.setValue(2)
        self.retry_delay_input.setSuffix("s")
        advanced_layout.addRow("Retry Delay:", self.retry_delay_input)
        
        # Rate limiting
        self.rate_limit_input = QSpinBox()
        self.rate_limit_input.setRange(0, 1000)
        self.rate_limit_input.setValue(60)
        self.rate_limit_input.setSuffix(" RPM")
        advanced_layout.addRow("Rate Limit:", self.rate_limit_input)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_config)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        
    def _load_current_config(self):
        """Load current configuration for selected model"""
        model_name = self.model_combo.currentText()
        if not model_name:
            return
            
        config = self.litellm_manager.get_model_config(model_name)
        if config:
            self.api_key_input.setText(config.get('api_key', ''))
            self.base_url_input.setText(
                config.get('provider_options', {}).get('api_base', '')
            )
            self.temperature_input.setValue(config.get('temperature', 0.7))
            self.max_tokens_input.setValue(config.get('max_tokens', 4096))
            self.timeout_input.setValue(config.get('timeout', 30))
            self.cache_checkbox.setChecked(config.get('cache_enabled', False))
        
    def _save_config(self):
        model_name = self.model_combo.currentText()
        
        if not model_name:
            QMessageBox.warning(self, "Error", "Model name is required")
            return
            
        config = {
            'name': model_name,
            'api_key': self.api_key_input.text(),
            'temperature': self.temperature_input.value(),
            'max_tokens': self.max_tokens_input.value(),
            'timeout': self.timeout_input.value(),
            'cache_enabled': self.cache_checkbox.isChecked(),
            'retry': {
                'count': self.retry_count_input.value(),
                'delay': self.retry_delay_input.value()
            },
            'rate_limit': self.rate_limit_input.value(),
            'provider_options': {
                'api_base': self.base_url_input.text(),
                'timeout': self.timeout_input.value()
            }
        }
        
        try:
            self.litellm_manager.update_model_config(model_name, config)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")