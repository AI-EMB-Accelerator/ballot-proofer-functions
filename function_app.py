"""Module to define the Azure Function App for proofing ballots."""

import logging
import azure.functions as func
from dotenv import load_dotenv

from utils.document import read_from_url


# Load environment variables from .env file
load_dotenv()

TEMP_FILE_URL = "https://ballotprooferstorage.blob.core.windows.net/ballots/ballot-type-1-english.pdf"

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="Hello")
@app.route(route="hello", methods=["GET"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP triggered function to say hello."""

    logging.info('Hello world triggered.')

    name = req.params.get('body')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}.")

    return func.HttpResponse(
            "Hello World!",
            status_code=200
    )

@app.function_name(name="ProofBallot")
@app.route(route="proof", methods=["POST"])
def proof_ballot(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP triggered function to proof a ballot."""

    logging.info('Proof ballot triggered.')

    # 1. Store ballot in blob storage -> Get URL
    # 2. Call Document Intelligence API to read the ballot
    # 3. Use Azure AI to define the ballot
    # 4. Proof the ballot
    # 5. Return the result

    return func.HttpResponse(
            "WHERE IS THE PROOF?",
            status_code=200
    )

@app.function_name(name="DefineBallot")
@app.route(route="define")
def define_ballot(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP triggered function to get a ballot definition."""

    logging.info('Defining a ballot triggered.')

    # 1. Store ballot in blob storage -> Get URL

    # 2. Call Document Intelligence API to read the ballot
    result = read_from_url(TEMP_FILE_URL)

    # 3. Use Azure AI to define the ballot
    # 4. Return the result

    if not result:
        return func.HttpResponse(
            "No ballot found.",
            status_code=404
        )

    return func.HttpResponse(
            result.content,
            status_code=200
    )
