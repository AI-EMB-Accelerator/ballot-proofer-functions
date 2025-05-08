"""AI-related utilities for parsing and generating ballot definitions."""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

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
            "content": "You are a ballot parser. You know NIST and CFM standards.",
        },
        {
            "role": "user",
            "content": "Define the ballot definition for the following content: 'This is a sample ballot content.'",
        }
    ],
    max_completion_tokens=800,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=deployment
)

print(response.choices[0].message.content)