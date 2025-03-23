from queue import PriorityQueue
from typing import Dict, Any
import time

class TaskQueue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.task_status = {}
        
    def add_task(self, task: Dict[str, Any], priority: int = 1):
        """Add a task to the queue with optional priority"""
        task_id = str(time.time_ns())
        task_data = {
            "id": task_id,
            "priority": priority,
            "status": "queued",
            "task": task
        }
        self.queue.put((-priority, task_data))
        self.task_status[task_id] = task_data
        return task_id
        
    def get_next_task(self):
        """Get the next highest priority task"""
        if not self.queue.empty():
            _, task = self.queue.get()
            task["status"] = "in_progress"
            self.task_status[task["id"]] = task
            return task
        return None
        
    def complete_task(self, task_id: str, result: Dict):
        """Mark a task as completed"""
        if task_id in self.task_status:
            self.task_status[task_id]["status"] = "completed"
            self.task_status[task_id]["result"] = result
            
    def fail_task(self, task_id: str, error: str):
        """Mark a task as failed"""
        if task_id in self.task_status:
            self.task_status[task_id]["status"] = "failed"
            self.task_status[task_id]["error"] = error
            
    def get_status(self, task_id: str):
        """Get status of a specific task"""
        return self.task_status.get(task_id)
        
    def get_all_status(self):
        """Get status of all tasks"""
        return self.task_status