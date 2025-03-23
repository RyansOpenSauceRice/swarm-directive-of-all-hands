from typing import Optional, Dict
from .openhands_client import OpenHandsClient

class Agent:
    def __init__(self, role: str, openhands_url: str):
        self.role = role
        self.client = OpenHandsClient(openhands_url)
        self.client.connect()
        
    def perform_task(self, task: Dict):
        """Execute a task based on agent role"""
        try:
            # Parse task
            command = task.get("command")
            params = task.get("parameters", {})
            
            # Execute command
            result = self.client.execute_command(command, params)
            
            # Handle result
            if result:
                return {"status": "success", "result": result}
            return {"status": "failed", "error": "No result returned"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
            
    def shutdown(self):
        self.client.close()