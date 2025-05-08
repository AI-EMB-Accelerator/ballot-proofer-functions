"""Module for managing storage operations."""

import os
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings


def save_to_blob_storage(file_path, blob_name):
    """
    Save a file to Azure Blob Storage.
    """
    account_url = os.getenv("AZURE_DOCUMENT_STORAGE_ENDPOINT") or ""
    credential = os.getenv("AZURE_DOCUMENT_STORAGE_KEY") or ""
    container_name = os.getenv("AZURE_DOCUMENT_STORAGE_CONTAINER_NAME") or ""

    if account_url is "" or credential is "" or container_name is "":
        raise ValueError("Please set the Azure Document environment variables")

    blob_service_client = BlobServiceClient(account_url, credential=credential)

    blob_name = f"{uuid.uuid4()}.pdf"

    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    with open(file_path, "rb") as file:
        blob_client.upload_blob(
            data=file,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/pdf"),
        )
    print(f"Document {blob_name} uploaded successfully")

    return f"{account_url}/{container_name}/{blob_name}"
