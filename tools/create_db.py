# This script is a modification from
# https://github.com/pixegami/langchain-rag-tutorial
# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
import os
import shutil

#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['LITELLM_API_KEY']
os.environ["OPENAI_BASE_URL"] = "https://lite-llm.mymaas.net/v1"

CHROMA_PATH = "chroma"
SRC_PATH = "../src"
TEST_PATH = "../tests"
LOGS_PATH = "../logs"


def main():
    generate_vector_store()


def generate_vector_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
  loader = DirectoryLoader(LOGS_PATH, glob="*.txt")
  logs = loader.load()
  
  loader = DirectoryLoader(SRC_PATH, glob="*.py")
  py_documents = loader.load()

  loader = DirectoryLoader(TEST_PATH, glob="*.py")
  test_documents = loader.load()
  
  documents = logs + py_documents + test_documents
  return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    #print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, 
        OpenAIEmbeddings(base_url="https://lite-llm.mymaas.net/v1", 
                        model="bedrock-cohere-embed-english-v3",
                        api_key=os.getenv("LITELLM_API_KEY")),
        persist_directory=CHROMA_PATH
    )
    db.persist()
    #print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()