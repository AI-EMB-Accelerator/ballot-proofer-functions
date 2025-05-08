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


def cleanup_tables(tables):
    """
    Cleans up the tables by removing empty cells and sorting them.
    """

    tables_out = []

    if tables:
        for table in ballot_layout.tables:
            # Collect cells with the required attributes
            cells = []
            for cell in table.cells:
                cells.append(
                    {
                        "page": cell.bounding_regions[0].page_number,
                        "column": cell.column_index,
                        "row": cell.row_index,
                        "content": cell.content,
                    }
                )

            # Sort cells by column first, then row
            sorted_cells = sorted(cells, key=lambda c: (c["column"], c["row"]))

            # Add to output tables list
            tables_out.append(sorted_cells)

    return tables_out


TEMP_FILE_URL = "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-english.pdf"

print("Reading from URL for Layout...")
ballot_layout = read_from_url(TEMP_FILE_URL, model_id="prebuilt-layout", pages="1-4")
organized_data = cleanup_tables(ballot_layout.tables)

print("Reading from URL for Content...")
backup_data = read_from_url(TEMP_FILE_URL, model_id="prebuilt-read", pages="1-4")

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

print(response.choices[0].message.content)
