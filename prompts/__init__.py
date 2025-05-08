""" "Loads the prompt for the ballot definition."""

from pathlib import Path

BALLOT_DEFINITION_PROMPT_NAME = "ballot-definition-prompt.txt"

ballot_definition_prompt = (
    Path(__file__).with_name(BALLOT_DEFINITION_PROMPT_NAME).read_text(encoding="utf-8")
)
