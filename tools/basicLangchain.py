import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

os.environ["OPENAI_BASE_URL"] = "https://lite-llm.mymaas.net/v1"

##############################################################
# Choose your model here:                                    #
#                                                            #
# gemini-flash is relatively smart, fast and inexpensive     #
# claude-3-5-sonnet is a more powerful model, but slower     #

# model = "claude-3-5-sonnet"
model = "gemini-flash"

##############################################################
# Choose the maximum size of the output here (in tokens)     #
max_output_tokens = 1000

#####################################################################
# Temperature is a parameter that controls the randomness of the    #
# output. Lower temperatures make the model more deterministic,     #
# while higher temperatures make the model more creative.           #
# Typically, temperature is a decimal number between 0 and 1.        #
# 0 = no creativity - good for repeating facts or generating lists  #
# 0.5 = moderate creativity - good for generating new sentences     #
# 1 = very creative - good for generating new ideas or text         #
temperature = 0.3

# Initialize the AzureOpenAI client
model = ChatOpenAI(model=model, api_key=os.getenv("LITELLM_API_KEY"))

# Send a completion call to generate an answer
user_query = "You are inside the repository: Python Hello World.\nThe GitHub Action workflow `python-tests.yaml` has encountered some failures.\nYour task is to identify the failures and analyze potential reasons for their occurrence.\nThe log attached is called `FAILURE_LOG.txt`.\nPlease output your findings in the following format:\n** Failure 1 **\n- Description of the failure:\n- Potential offending files:\n- Possible reasons for the failure:\n** Failure 2 **\n- Description of the failure:\n- Potential offending files:\n- Possible reasons for the failure:\n(Continue as needed for additional failures)\n"

response = model.invoke(
    [
        # System Message is optional
        SystemMessage("You are a helpful assistant."),
        HumanMessage(user_query),
    ],
    temperature=temperature,
    max_tokens=max_output_tokens,
)

print(f"{user_query}\n\n{response.content}")
