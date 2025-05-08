"""This module provides a function to read a document from a URL."""

import os
from typing import Optional, Literal
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

ModelId = Literal["prebuilt-layout", "prebuilt-read"]


def read_from_url(
    url: str, model_id: Optional[ModelId] = "prebuilt-read", pages: Optional[str] = None
) -> AnalyzeDocumentRequest:
    """
    This function reads a document from a URL using the Azure Document Intelligence client.
    """

    endpoint: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
    key: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

    if endpoint == "" or key == "":
        raise ValueError(
            "Please set the Azure Document Intelligence environment variables"
        )

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        model_id=model_id, body=AnalyzeDocumentRequest(url_source=url), pages=pages
    )

    result = poller.result()

    return result
