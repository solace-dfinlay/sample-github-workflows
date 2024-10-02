# Python LiteLLM starter project

Here are some basic examples of how to use the LiteLLM API to call our models.

* **basic.py** - this uses the openai api to call our litellm API. Probably the simplest to use.
* **basicLangchain.py** - this uses langchain to call our litellm API. Opens the door to more complex abstractions with Langchain like RAG

## How to run the examples

```
git clone https://github.com/solace-dfinlay/sample-github-workflows.git
cd sample-github-workflows
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export LITELLM_API_KEY=<YOUR_LITELLM_API_KEY>

python tools/basic.py
python tools/basicLangchain.py
```

## Python3

You may need to alias python to python3 and pip to pip3 depending on your installation:
```
alias python=python3
alias pip=pip3
```