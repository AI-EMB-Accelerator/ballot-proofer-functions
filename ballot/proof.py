"""Proofing the ballot using the test and reference definitions."""

from ..ai.prompts import ballot_proof_prompt
from ..ai.chat import send_prompt
from ..ai.document import read_from_url


def proof_ballot(test_definition, reference_definition):
    """
    This function proofs the ballot using the test and reference definitions.
    """

    proof = send_prompt(
        ballot_proof_prompt,
        f"Proof this ballot using REFERENCE BALLOT DEFINITION '{reference_definition}' and the TEST BALLOT DEFINITION '{test_definition}'",
        True,
    )
    return proof

def locate_proof_errors(proof, ballot_url, pages="1"):
    """
    Locate proof errors in the ballot data.
    """

    ballot_data = read_from_url(ballot_url, model_id="prebuilt-read", pages=pages)

    proof = send_prompt(
        ballot_proof_prompt,
        f"Find the error boxes in this data: '{ballot_data}' for the errors in this proof: '{proof}'",
    )
    return proof
