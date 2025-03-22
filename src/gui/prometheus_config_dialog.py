from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox,
    QCheckBox, QDialogButtonBox, QMessageBox
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.config_manager import ConfigManager

class PrometheusConfigDialog(QDialog):
    def __init__(self, config: 'ConfigManager', parent=None):
        super().__init__(parent)
        self.config = config
        self._setup_ui()
        
    def _setup_ui(self):
        self.setWindowTitle("Prometheus Configuration")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Enable/disable toggle
        self.enable_checkbox = QCheckBox("Enable Prometheus Monitoring")
        form_layout.addRow(self.enable_checkbox)
        
        # Port configuration
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        form_layout.addRow("Prometheus Port:", self.port_input)
        
        # Remote URL
        self.remote_url_input = QLineEdit()
        self.remote_url_input.setPlaceholderText("http://prometheus.example.com:9090")
        form_layout.addRow("Remote Prometheus URL:", self.remote_url_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_config)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        self._load_current_config()
        
    def _load_current_config(self):
        """Load current configuration"""
        config = self.config.get('monitoring.prometheus', {})
        self.enable_checkbox.setChecked(config.get('enabled', True))
        self.port_input.setValue(config.get('port', 8000))
        self.remote_url_input.setText(config.get('remote_url', ''))
        
    def _save_config(self):
        """Save configuration"""
        config = {
            'enabled': self.enable_checkbox.isChecked(),
            'port': self.port_input.value(),
            'remote_url': self.remote_url_input.text()
        }
        
        try:
            self.config.set('monitoring.prometheus', config)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")