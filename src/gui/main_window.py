from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QStatusBar, QMenuBar, QMenu,
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget
)
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING
from .litellm_config_dialog import LiteLLMConfigDialog

if TYPE_CHECKING:
    from core.config_manager import ConfigManager
    from utils.i18n import Localization
    from core.agent_manager import AgentManager
    from core.litellm_manager import LiteLLMManager

class MainWindow(QMainWindow):
    def __init__(self, config: 'ConfigManager', i18n: 'Localization', agent_manager: 'AgentManager'):
        super().__init__()
        self.config = config
        self.i18n = i18n
        self.agent_manager = agent_manager
        self._setup_ui()
        self._setup_menu()
        self._load_config()
        
    def _setup_ui(self):
        self.setWindowTitle(self.i18n.gettext("OpenHands Swarm Controller"))
        self.resize(1200, 800)
        
        # Create main tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create agent management tab
        self.agent_tab = QWidget()
        self.agent_tab_layout = QVBoxLayout()
        
        # Agent list
        self.agent_list = QListWidget()
        self.agent_tab_layout.addWidget(self.agent_list)
        
        # Agent controls
        control_layout = QHBoxLayout()
        self.add_agent_button = QPushButton(self.i18n.gettext("Add Agent"))
        self.remove_agent_button = QPushButton(self.i18n.gettext("Remove Agent"))
        control_layout.addWidget(self.add_agent_button)
        control_layout.addWidget(self.remove_agent_button)
        self.agent_tab_layout.addLayout(control_layout)
        
        self.agent_tab.setLayout(self.agent_tab_layout)
        self.tabs.addTab(self.agent_tab, self.i18n.gettext("Agents"))
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Connect signals
        self.add_agent_button.clicked.connect(self._add_agent)
        self.remove_agent_button.clicked.connect(self._remove_agent)
        
    def _setup_menu(self):
        menu_bar = QMenuBar(self)
        
        # File menu
        file_menu = QMenu(self.i18n.gettext("&File"), self)
        file_menu.addAction(self.i18n.gettext("&Settings"))
        file_menu.addSeparator()
        file_menu.addAction(self.i18n.gettext("E&xit"))
        menu_bar.addMenu(file_menu)
        
        # View menu
        view_menu = QMenu(self.i18n.gettext("&View"), self)
        self.theme_menu = view_menu.addMenu(self.i18n.gettext("&Theme"))
        self.language_menu = view_menu.addMenu(self.i18n.gettext("&Language"))
        menu_bar.addMenu(view_menu)
        
        # Tools menu
        tools_menu = QMenu(self.i18n.gettext("&Tools"), self)
        tools_menu.addAction(self.i18n.gettext("Configure LiteLLM"), self._configure_litellm)
        tools_menu.addAction(self.i18n.gettext("Configure Monitoring"), self._configure_monitoring)
        menu_bar.addMenu(tools_menu)
        
        self.setMenuBar(menu_bar)

    def _configure_monitoring(self):
        """Open monitoring configuration dialog"""
        from .prometheus_config_dialog import PrometheusConfigDialog
        dialog = PrometheusConfigDialog(self.config, self)
        if dialog.exec():
            self.status_bar.showMessage("Monitoring configuration updated", 3000)
        
    def _configure_litellm(self):
        """Open LiteLLM configuration dialog"""
        dialog = LiteLLMConfigDialog(self.agent_manager.litellm_manager, self)
        if dialog.exec():
            self.status_bar.showMessage("LiteLLM configuration updated", 3000)
        
    def _load_config(self):
        # Apply theme
        theme = self.config.get('ui.theme', 'dark')
        self._apply_theme(theme)
        
        # Setup language menu
        self._setup_language_menu()
        
        # Load agents
        self._load_agents()
        
    def _apply_theme(self, theme: str):
        if theme == 'dark':
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
            """)
        else:
            self.setStyleSheet("")
            
    def _setup_language_menu(self):
        for lang in self.i18n.get_available_languages():
            action = self.language_menu.addAction(lang)
            action.triggered.connect(
                lambda _, l=lang: self._change_language(l)
            )
            
    def _change_language(self, language_code: str):
        if self.i18n.set_language(language_code):
            self.config.set('ui.language', language_code)
            self.retranslate_ui()
            
    def _load_agents(self):
        self.agent_list.clear()
        for agent_name in self.agent_manager.agents.keys():
            self.agent_list.addItem(agent_name)
            
    def _add_agent(self):
        # TODO: Implement agent creation dialog
        pass
        
    def _remove_agent(self):
        selected = self.agent_list.currentItem()
        if selected:
            agent_name = selected.text()
            self.agent_manager.remove_agent(agent_name)
            self._load_agents()
            
    def retranslate_ui(self):
        self.setWindowTitle(self.i18n.gettext("OpenHands Swarm Controller"))
        self.menuBar().actions()[0].setText(self.i18n.gettext("&File"))
        self.menuBar().actions()[1].setText(self.i18n.gettext("&View"))
        self.menuBar().actions()[2].setText(self.i18n.gettext("&Tools"))
        self.add_agent_button.setText(self.i18n.gettext("Add Agent"))
        self.remove_agent_button.setText(self.i18n.gettext("Remove Agent"))
        self.tabs.setTabText(0, self.i18n.gettext("Agents"))