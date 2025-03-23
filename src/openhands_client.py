from playwright.sync_api import sync_playwright
from typing import Optional

class OpenHandsClient:
    def __init__(self, url: str = "http://localhost:51090"):
        self.url = url
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
    def connect(self):
        self.page.goto(self.url)
        # Wait for OpenHands to load
        self.page.wait_for_selector("#openhands-container")
        
    def execute_command(self, command: str, params: Optional[dict] = None):
        """Execute a command through the OpenHands interface"""
        try:
            # Find command input
            self.page.fill("#command-input", command)
            
            # If parameters exist, fill them
            if params:
                for key, value in params.items():
                    self.page.fill(f"#{key}-input", str(value))
                    
            # Execute command
            self.page.click("#execute-button")
            
            # Wait for response
            self.page.wait_for_selector("#response-container")
            
            # Return response
            return self.page.inner_text("#response-container")
        except Exception as e:
            print(f"Command execution failed: {str(e)}")
            return None
        
    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()