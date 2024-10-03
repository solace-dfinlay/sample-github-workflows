import os
import sys
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
import openai
from create_db import generate_vector_store

LITELLM_API_KEY = os.getenv('LITELLM_API_KEY')

PROMPT_TEMPLATE = """
Context: {context}

---

Question: {question}

"""

class AIAgent:
    def __init__(self):
        # Set environment variables
        os.environ["OPENAI_BASE_URL"] = "https://lite-llm.mymaas.net/v1"
  
        # Configuration
        self.model_name = "claude-3-5-sonnet"
        self.max_output_tokens = 1000
        self.temperature = 0.3
        self.chroma_path = "chroma"
        
        # Load logs and source code into Chroma vector store
        generate_vector_store()

    def analyze_logs(self):
        query_text = "You are reviewing the repository: Sample Github Workflows. The GitHub Action workflow python-tests.yaml has failed. Answer the question based only on the following context:\n\n{context}\nYour task:\n\nIdentify each failure in the failed workflow.\nAnalyze and explain the possible reasons for the failures.\nAttached: Workflow logs and repository source code.\n\nPlease provide your findings in this format:\n\nFailure 1\nDescription: What went wrong?\nPotential causes: Which files or code segments are likely responsible?\nRoot cause: Why did this failure occur?\n\nFailure 2\nDescription:\nPotential causes:\nRoot cause:\n(Continue for all identified failures)\n\n---\n\n"
        
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
        formatted_response = f"{response_text}\nSources: {sources}"
        return formatted_response

def main():
    # Initialize the AI agent
     # Get the API key from environment variable
    agent = AIAgent()
    
    # Analyze the logs
    analysis_result = agent.analyze_logs()
    
    # Check if analysis_result is not empty
    if analysis_result:
        print(analysis_result)
    else:
        print("No content found.")

if __name__ == "__main__":
    main()