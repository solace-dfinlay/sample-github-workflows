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
        prompt_file_path = "prompt_config.txt"

        with open(prompt_file_path, 'r') as file:
            prompt = file.read()

        user_query = f"{prompt}\n\n{logs}"
        
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
    LITELLM_API_KEY = os.getenv('LITELLM_API_KEY')  # Get the API key from environment variable
    agent = AIAgent(LITELLM_API_KEY)
    
    # Read the logs from the file
    with open(log_file_path, 'r') as log_file:
        logs = log_file.read()
    
    # Analyze the logs
    analysis_result = agent.analyze_logs(logs)
    
    # Check if analysis_result has a 'content' attribute (for AIMessage type)
    if hasattr(analysis_result, 'content'):
        content = analysis_result.content
        print(content)
    else:
        print("No content found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ai_agent.py <log_file_path>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    main(log_file_path)