"""Demonstrate getting definition from a ballot"""

from dotenv import load_dotenv

from ballot.define import get_definition

load_dotenv()

OUTPUT_FILE = "ballot_definition.json"
PAGES = "1"
BALLOT_URL = "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-english.pdf"

ballot_definition = get_definition(BALLOT_URL, pages=PAGES)

with open(f"./output/definitions/{OUTPUT_FILE}", "w", encoding="utf-8") as f:
    f.write(ballot_definition)
