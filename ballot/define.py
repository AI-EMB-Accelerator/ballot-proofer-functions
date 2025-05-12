"""Module to define the ballot using Azure AI."""

from typing import Optional
from ai.document import read_from_url, cleanup_tables
from ai.chat import send_prompt
from ai.prompts import ballot_definition_prompt


def get_definition(ballot_url: str, pages: Optional[str] = "1") -> str:
    """
    This function gets the ballot definition from the Azure AI.
    """

    ballot_layout = read_from_url(ballot_url, model_id="prebuilt-layout", pages=pages)
    ballot_data = read_from_url(ballot_url, model_id="prebuilt-read", pages=pages)

    sanitized_layout_data = cleanup_tables(ballot_layout.tables or [])

    definition = send_prompt(
        ballot_definition_prompt,
        f"Define the ballot definition using this PRIMARY LAYOUT: '{sanitized_layout_data}' and this BACKUP LAYOUT: '{ballot_data}'",
    )

    return definition
