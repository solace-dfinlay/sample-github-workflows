import os
import sys
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class AIAgent:
    def __init__(self, llm_api_key):
        # Set environment variables
        os.environ["OPENAI_BASE_URL"] = "https://lite-llm.mymaas.net/v1"
        
        # Configuration
        self.model_name = "claude-3-5-sonnet"
        self.max_output_tokens = 1000
        self.temperature = 0.3
        
        # Initialize the LLM client
        self.model = ChatOpenAI(model=self.model_name, api_key=llm_api_key)
    
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
    # Initialize the AI agent
    api_key = os.getenv('API_KEY')  # Get the API key from environment variable
    agent = AIAgent(api_key)
    
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