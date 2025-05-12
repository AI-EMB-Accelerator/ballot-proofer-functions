"""Module for interacting with the OpenAI API."""

import os
from openai import AzureOpenAI


def send_prompt(system_prompt, user_prompt, reasoning=False):
    """Queue an AI prompt to the Azure OpenAI API."""

    token_limit = 32000
    endpoint = os.getenv("AZURE_OPEN_AI_ENDPOINT", "")
    deployment = os.getenv("AZURE_OPEN_AI_DEPLOYMENT", "")
    subscription_key = os.getenv("AZURE_OPEN_AI_KEY", "")
    api_version = os.getenv("AZURE_OPEN_AI_API_VERSION", "")

    if reasoning is True:
        token_limit = 20000
        endpoint = os.getenv("O3_AZURE_OPEN_AI_ENDPOINT", "")
        deployment = os.getenv("O3_AZURE_OPEN_AI_DEPLOYMENT", "")
        subscription_key = os.getenv("O3_AZURE_OPEN_AI_KEY", "")
        api_version = os.getenv("O3_AZURE_OPEN_AI_API_VERSION", "")

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        response_format={"type": "json_object"},
        max_completion_tokens=token_limit,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=deployment,
    )

    return response.choices[0].message.content
