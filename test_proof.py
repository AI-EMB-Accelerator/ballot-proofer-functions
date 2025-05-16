import json
import time
from dotenv import load_dotenv

from ballot.define import get_definition
from ballot.proof import proof_ballot

load_dotenv()

# Define all ballots to be processed
ballot_jobs = [
    {
        "title": "Correct Definition",
        "input_path": "./input/definitions/ballot_definition.json",
        "output_path": "./output/proofs/ballot_proof.json",
        "ballot_url": "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-english.pdf",
        "pages": "1"
    },
    {
        "title": "Wrong Definition - With manual errors",
        "input_path": "./input/definitions/ballot_definition_wrong.json",
        "output_path": "./output/proofs/ballot_proof_wrong.json",
        "ballot_url": "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-english.pdf",
        "pages": "1"
    }
]

for job in ballot_jobs:
    print(f"\n=== Processing {job['title']} ===")

    timers = {}

    # Step 1: Define ballot
    print("Defining ballot...")
    start = time.time()
    test_definition = get_definition(job["ballot_url"], pages=job["pages"])
    timers["definition"] = time.time() - start
    print(f"Ballot definition took {timers['definition']:.2f} seconds")

    # Step 2: Load reference definition
    print("Loading reference definition...")
    start = time.time()
    with open(job["input_path"], "r", encoding="utf-8") as file:
        reference_definition = json.load(file)
    timers["load_reference"] = time.time() - start
    print(f"Reference loading took {timers['load_reference']:.2f} seconds")

    # Step 3: Proof ballot
    print("Proofing ballot...")
    start = time.time()
    proof = proof_ballot(test_definition, reference_definition)
    timers["proofing"] = time.time() - start
    print(f"Ballot proofing took {timers['proofing']:.2f} seconds")

    # Step 4: Save proof
    print("Saving proof...")
    start = time.time()
    with open(job["output_path"], "w", encoding="utf-8") as f:
        f.write(proof)
    timers["saving"] = time.time() - start
    print(f"Proof saving took {timers['saving']:.2f} seconds")

    total = sum(timers.values())
    print(f"Total time for {job['output_path']}: {total:.2f} seconds")