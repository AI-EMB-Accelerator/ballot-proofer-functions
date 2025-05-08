"""AI-related utilities for parsing and generating ballot definitions."""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from pprint import pp


from prompts import ballot_definition_prompt
from utils.document import read_from_url

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

# Step 1 - Get the Content of the ballot
# Ballot Content - The content of the ballot after its parsed by Document Intelligence

# Step 2 - Get the Ballot Definition
# Ballot Definition - NIST Definition of what needs to be in a ballot

# Step 3 - Proof
# Inputs - Ballot Definition OFFICIAL, Ballot Content, Ballot Definition (Parsed)

TEMP_FILE_URL = "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-english-no-page-1.pdf"

ballot_content = read_from_url(TEMP_FILE_URL)

for var in vars(ballot_content):
    pp(var, depth=1)
    print()

for table in ballot_content.tables:
    print("Table: =====================")
    pp(table, depth=1)
    print()

# print("CONTENT =====================")
# print(ballot_content)

# response = client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",
#             "content": ballot_definition_prompt,
#         },
#         {
#             "role": "user",
#             "content": f"Define the ballot definition for the following content: {ballot_content}'",
#         },
#     ],
#     response_format={"type": "json_object"},
#     max_completion_tokens=32000,
#     temperature=1.0,
#     top_p=1.0,
#     frequency_penalty=0.0,
#     presence_penalty=0.0,
#     model=deployment,
# )

# print(response.choices[0].message.content)
