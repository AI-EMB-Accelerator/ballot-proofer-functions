"""Module to get the ballot definition"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from prompts import ballot_definition_prompt

load_dotenv()

def get_definition(ballot_content):
    """
    This function gets the ballot definition from the Azure AI.
    It uses the Azure OpenAI API to get the ballot definition.
    """
    endpoint = os.getenv("AZURE_OPEN_AI_ENDPOINT", "")
    # model_name = "gpt-4.1-mini"
    deployment = os.getenv("AZURE_OPEN_AI_DEPLOYMENT", "")

    subscription_key = os.getenv("AZURE_OPEN_AI_KEY", "")
    api_version = os.getenv("AZURE_OPEN_AI_API_VERSION", "")

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": ballot_definition_prompt,
            },
            {
                "role": "user",
                "content": f"Define the ballot definition for the following content: '{ballot_content}'",
            }
        ],
        max_completion_tokens=800,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=deployment
    )

    return response.choices[0].message.content
