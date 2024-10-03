import os
import sys
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from create_db import generate_data_store
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
import openai
import os

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}
You are reviewing the repository: Python Hello World.
The GitHub Action workflow python-tests.yaml has failed.

Your task:

Identify each failure in the workflow.
Analyze and explain the possible reasons for the failures.
Attached: Workflow logs and repository source code.

Please provide your findings in this format:

Failure 1
Description: What went wrong?
Potential causes: Which files or code segments are likely responsible?
Root cause: Why did this failure occur?

Failure 2
Description:
Potential causes:
Root cause:

(Continue for all identified failures)

---

"""

class AIAgent:
    def __init__(self):
        # Set environment variables
        self.chroma_path = "chroma"
        openai.api_key = os.environ['LITELLM_API_KEY']
        os.environ["OPENAI_BASE_URL"] = "https://lite-llm.mymaas.net/v1"
        
        # Configuration
        self.model_name = "claude-3-5-sonnet"
        self.max_output_tokens = 1000
        self.temperature = 0.3
        self.chroma_path = "chroma"
        # Initialize the LLM client
        # self.model = ChatOpenAI(model=self.model_name, api_key=llm_api_key)
        generate_data_store()


    def create_response(self):
      query_text = "What is the failure in this GitHub Actions log?"
      # Prepare the DB.
      embedding_function = OpenAIEmbeddings(base_url="https://lite-llm.mymaas.net/v1", model="bedrock-cohere-embed-english-v3", api_key=os.getenv("LITELLM_API_KEY"))
      db = Chroma(persist_directory=self.chroma_path, embedding_function=embedding_function)

      # Search the DB.
      results = db.similarity_search_with_score(query_text, k=5)
      context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
      prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
      prompt = prompt_template.format(context=context_text, question=query_text)

      #print(prompt)

      model = ChatOpenAI(model=self.model_name, api_key=os.getenv("LITELLM_API_KEY"))
      response_text = model.predict(prompt)

      sources = [doc.metadata.get("source", None) for doc, _score in results]
      formatted_response = f"Response: {response_text}\nSources: {sources}"
      print(formatted_response)


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

def main():
    """
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

    """
    agent = AIAgent()
    agent.create_response()   

if __name__ == "__main__":
    main()
    if len(sys.argv) != 2:
        print("Usage: python dylan_ai_agent.py <log_file_path>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    main(log_file_path)