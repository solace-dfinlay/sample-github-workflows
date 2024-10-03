import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai
import os

CHROMA_PATH = "chroma"

openai.api_key = os.environ['LITELLM_API_KEY']
os.environ["OPENAI_BASE_URL"] = "https://lite-llm.mymaas.net/v1"


user_query = "You are inside the repository: Python Hello World.\nThe GitHub Action workflow `python-tests.yaml` has encountered some failures.\nYour task is to identify the failures and analyze potential reasons for their occurrence.\nThe log attached is called `FAILURE_LOG.txt`.\nPlease output your findings in the following format:\n** Failure 1 **\n- Description of the failure:\n- Potential offending files:\n- Possible reasons for the failure:\n** Failure 2 **\n- Description of the failure:\n- Potential offending files:\n- Possible reasons for the failure:\n(Continue as needed for additional failures)\n"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}
You are inside the repository: Python Hello World.\nThe GitHub Action workflow `python-tests.yaml` has encountered some failures.\nYour task is to identify the failures and analyze potential reasons for their occurrence.\nThe log attached is called `FAILURE_LOG.txt`.\nPlease output your findings in the following format:\n** Failure 1 **\n- Description of the failure:\n- Potential offending files:\n- Possible reasons for the failure:\n** Failure 2 **\n- Description of the failure:\n- Potential offending files:\n- Possible reasons for the failure:\n(Continue as needed for additional failures)\n

---

{question}
"""


def main():
    # Create CLI.
    query_text = "What is the failure in this GitHub Actions log?"
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(base_url="https://lite-llm.mymaas.net/v1", model="bedrock-cohere-embed-english-v3", api_key=os.getenv("LITELLM_API_KEY"))
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    print(prompt)

    model = ChatOpenAI(model="gemini-flash", api_key=os.getenv("LITELLM_API_KEY"))
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()