import os
import sys
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

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
        return response

def main(log_file_path):
    # Configuration for the AI agent
    model_name = "your-model-name"
    api_key = "your-api-key"
    base_url = "your-base-url"
    
    # Initialize the AI agent
    agent = AIAgent(model_name, api_key, base_url)
    
    # Read the logs from the file
    with open(log_file_path, 'r') as log_file:
        logs = log_file.read()
    
    # Analyze the logs
    analysis_result = agent.analyze_logs(logs)
    
    # Print the analysis result
    print(analysis_result)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dylan_ai_agent.py <log_file_path>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    main(log_file_path)