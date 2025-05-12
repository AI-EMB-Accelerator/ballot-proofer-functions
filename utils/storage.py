"""Module for managing storage operations."""

import os
import uuid
from typing import Tuple
from azure.storage.blob import BlobServiceClient, ContentSettings, BlobClient


def _get_blob_client(blob_name: str) -> Tuple[BlobClient, str]:
    """
    Get the Blob Client and URL for Azure Blob Storage.
    """
    account_url = os.getenv("AZURE_DOCUMENT_STORAGE_ENDPOINT") or ""
    credential = os.getenv("AZURE_DOCUMENT_STORAGE_KEY") or ""
    container_name = os.getenv("AZURE_DOCUMENT_STORAGE_CONTAINER_NAME") or ""

    if account_url == "" or credential == "" or container_name == "":
        raise ValueError("Please set the Azure Document environment variables")

    blob_service_client = BlobServiceClient(account_url, credential=credential)

    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    blob_url = f"{account_url}/{container_name}/{blob_name}"

    return (blob_client, blob_url)


def save_to_blob_storage(file_path) -> str:
    """
    Save a file to Azure Blob Storage.
    """

    blob_name = f"{uuid.uuid4()}.pdf"
    blob_client, blob_url = _get_blob_client(blob_name)

    with open(file_path, "rb") as file:
        blob_client.upload_blob(
            data=file,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/pdf"),
        )

    return blob_url


def save_data_to_blob_storage(data, blob_name) -> str:
    """
    Save a file to Azure Blob Storage.
    """

    blob_name = f"{uuid.uuid4()}.json"
    blob_name = f"{uuid.uuid4()}.pdf"
    blob_client, blob_url = _get_blob_client(blob_name)

    blob_client.upload_blob(
        data=data,
        overwrite=True,
    )

    return blob_url
