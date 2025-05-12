""" "Loads the prompt for the ballot definition."""

from pathlib import Path

BALLOT_DEFINITION_PROMPT_NAME = "ballot-definition-prompt.txt"
BALLOT_PROOF_PROMPT_NAME = "ballot-proof-prompt.txt"
ERROR_BOX_PROMPT_NAME = "error-box-prompt.txt"

ballot_definition_prompt = (
    Path(__file__).with_name(BALLOT_DEFINITION_PROMPT_NAME).read_text(encoding="utf-8")
)

ballot_proof_prompt = (
    Path(__file__).with_name(BALLOT_PROOF_PROMPT_NAME).read_text(encoding="utf-8")
)

error_box_prompt = (
    Path(__file__).with_name(ERROR_BOX_PROMPT_NAME).read_text(encoding="utf-8")
)
