"""Demonstrate proofing a ballot against a reference definition"""

import json
from dotenv import load_dotenv

from ballot.define import get_definition
from ballot.proof import proof_ballot

load_dotenv()

INPUT_PATH = "./input/definitions/ballot_definition.json"
OUTPUT_PATH = "./output/proofs/ballot_proof.json"
PAGES = "1"
BALLOT_URL = "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-english.pdf"

test_definition = get_definition(BALLOT_URL, pages=PAGES)

with open(INPUT_PATH, "r", encoding="utf-8") as file:
    reference_definition = json.load(file)

proof = proof_ballot(test_definition, reference_definition)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(proof)
