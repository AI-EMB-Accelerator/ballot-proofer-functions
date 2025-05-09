"""AI-related utilities for parsing and generating ballot definitions."""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI


from prompts import ballot_definition_prompt
from utils.document import read_from_url, cleanup_tables
from utils.storage import save_data_to_blob_storage

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


OUTPUT_FILE = "ballot_definition.json"
PAGES = "1-4"

BALLOT_FILE_1_ENGLISH = "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-english.pdf"
BALLOT_FILE_2_SPANISH = "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-spanish.pdf"

ballot_layout = read_from_url(BALLOT_FILE_1_ENGLISH, model_id="prebuilt-layout", pages=PAGES)
organized_data = cleanup_tables(ballot_layout.tables or [])

backup_data = read_from_url(BALLOT_FILE_1_ENGLISH, model_id="prebuilt-read", pages=PAGES)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": ballot_definition_prompt,
        },
        {
            "role": "user",
            "content": f"Define the ballot definition using this PRIMARY LAYOUT: '{organized_data}' and this BACKUP LAYOUT: '{backup_data}'",
        },
    ],
    response_format={"type": "json_object"},
    max_completion_tokens=32000,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=deployment,
)

ballot_definition = response.choices[0].message.content

with open(f"./output/definitions/{OUTPUT_FILE}", "w") as f:
    f.write(ballot_definition)

# # output to json file
# file = save_data_to_blob_storage(response.choices[0].message.content, OUTPUT_FILE) 