from typing import Dict, Any
from agents import Agent, Runner
from .litellm_manager import LiteLLMManager
from .config_manager import ConfigManager

class AgentManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.agents: Dict[str, Agent] = {}
        self.litellm_manager = LiteLLMManager(config)
        
    def create_agent(self, name: str, instructions: str, tools: list = None, model: str = None):
        """Create a new agent with optional model configuration"""
        if model is None:
            model = self.litellm_manager.get_default_model()
            
        agent = Agent(
            name=name,
            instructions=instructions,
            tools=tools or [],
            max_turns=self.config.get('agents.max_turns', 10),
            model=model
        )
        self.agents[name] = agent
        return agent
        
    async def run_agent(self, agent_name: str, input_text: str):
        """Execute an agent with the given input"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
            
        agent = self.agents[agent_name]
        return await Runner.run(agent, input=input_text)
        
    def get_agent(self, agent_name: str) -> Agent:
        """Get an agent by name"""
        return self.agents.get(agent_name)
        
    def remove_agent(self, agent_name: str):
        """Remove an agent by name"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            
    def get_available_models(self) -> list[str]:
        """Get available LiteLLM models"""
        return self.litellm_manager.get_available_models()
        
    def update_agent_model(self, agent_name: str, model_name: str):
        """Update the model for an existing agent"""
        if agent_name in self.agents:
            self.agents[agent_name].model = model_name