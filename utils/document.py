"""This module provides a function to read a document from a URL."""

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest


def read_from_url(url: str):
    """
    This function reads a document from a URL using the Azure Document Intelligence client.
    """

    endpoint: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT") or ""
    key: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY") or ""

    if endpoint is "" or key is "":
        raise ValueError(
            "Please set the Azure Document Intelligence environment variables"
        )

    document_intelligence_client  = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read", AnalyzeDocumentRequest(url_source=url)
    )

    result = poller.result()
    print("Document contains content: ", result)

    return result
