from typing import Dict, Any
from datetime import datetime
import json

class Monitor:
    def __init__(self):
        self.metrics = {
            "tasks_processed": 0,
            "tasks_failed": 0,
            "tasks_completed": 0,
            "start_time": datetime.now().isoformat()
        }
        
    def log_task(self, task_id: str, status: str, details: Dict[str, Any]):
        """Log task status and details"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "task_id": task_id,
            "status": status,
            "details": details
        }
        
        # Update metrics
        if status == "completed":
            self.metrics["tasks_completed"] += 1
        elif status == "failed":
            self.metrics["tasks_failed"] += 1
        self.metrics["tasks_processed"] += 1
        
        # Print log (could be replaced with file/DB logging)
        print(json.dumps(log_entry, indent=2))
        
    def get_metrics(self):
        """Get current system metrics"""
        return self.metrics
        
    def get_status(self):
        """Get system status summary"""
        return {
            "uptime": str(datetime.now() - datetime.fromisoformat(self.metrics["start_time"])),
            **self.metrics
        }