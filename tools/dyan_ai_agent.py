import os
import sys
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

class AIAgent:
    def __init__(self, model_name, api_key, base_url, max_output_tokens=1000, temperature=0.3):
        # Set environment variables
        os.environ["OPENAI_BASE_URL"] = base_url
        
        # Configuration
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        
        # Initialize the LLM client
        self.model = ChatOpenAI(model=model_name, api_key=api_key)
    
    def analyze_logs(self, logs):
        user_query = f"Analyze the following logs and explain the error and possible solution:\n\n{logs}"
        
        response = self.model.invoke(
            [
                SystemMessage("You are a helpful assistant."),
                HumanMessage(user_query),
            ],
            temperature=self.temperature,
            max_tokens=self.max_output_tokens,
        )
        
        return response.content
    
    def read_logs(self):
        return sys.stdin.read()
    
    def print_analysis(self, analysis):
        print(analysis)

if __name__ == '__main__':
    # Initialize the AI agent
    ai_agent = AIAgent(
        model_name="claude-3-5-sonnet",
        api_key=os.getenv("LITELLM_API_KEY"),
        base_url="https://lite-llm.mymaas.net/v1"
    )
    
    # Read logs from standard input
    logs = ai_agent.read_logs()
    
    # Analyze the logs
    analysis = ai_agent.analyze_logs(logs)
    
    # Print the analysis result
    ai_agent.print_analysis(analysis)