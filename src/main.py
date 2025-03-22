import sys
import asyncio
from PySide6.QtWidgets import QApplication
from utils.i18n import Localization
from core.config_manager import ConfigManager
from core.agent_manager import AgentManager
from gui.main_window import MainWindow

def main():
    # Initialize application
    app = QApplication(sys.argv)
    
    # Load configuration
    config = ConfigManager('config/config.json')
    
    # Initialize localization
    i18n = Localization(config.config_path)
    i18n.set_language(config.get('ui.language'))
    
    # Initialize agent manager
    agent_manager = AgentManager(config)
    
    # Create default agents
    agent_manager.create_agent(
        name="Swarm Controller",
        instructions="You are the main controller for the OpenHands swarm"
    )
    
    # Create and show main window
    window = MainWindow(config, i18n, agent_manager)
    window.show()
    
    # Start application loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()