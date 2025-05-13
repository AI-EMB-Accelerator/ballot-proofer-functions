"""Module to define the Azure Function App for proofing ballots."""

import json
import logging
import tempfile
import azure.functions as func
from dotenv import load_dotenv

from ballot.define import get_definition
from ballot.proof import proof_ballot, locate_proof_errors
from utils.storage import save_to_blob_storage


# Load environment variables from .env file
load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name(name="Hello")
@app.route(route="hello", methods=["GET"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP triggered function to say hello."""

    logging.info("Hello world triggered.")

    name = req.params.get("body")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(f"Hello, {name}.")

    return func.HttpResponse("Hello World!", status_code=200)


@app.function_name(name="ProofBallot")
@app.route(route="proof", methods=["POST"])
def proof_ballot_api(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP triggered function to proof a ballot."""

    logging.info("Proof ballot triggered.")

    try:
        # Validate inputs
        ballot = req.files.get("ballot")
        reference = req.form.get("reference") or "{}"
        pages = req.form.get("pages") or "1"
        locators = req.form.get("locators") == "true"

        if not ballot or not reference:
            return func.HttpResponse(
                "Missing 'ballot' or 'reference' in form-data", status_code=400
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(ballot.stream.read())
            ballot_path = tmp_file.name

        blob_url = save_to_blob_storage(ballot_path)
        logging.info("Ballot uploaded to blob storage: %s", blob_url)

        reference_ballot_definition = reference

        test_ballot_definition = get_definition(blob_url, pages=pages)
        proof = proof_ballot(test_ballot_definition, reference_ballot_definition)
        locators = (
            locate_proof_errors(proof, blob_url, pages=pages) if locators else None
        )

        response = {
            "proof": json.loads(proof),
            "locators": locators,
            "ballot_url": blob_url,
        }
        body = json.dumps(response)

        return func.HttpResponse(
            body,
            mimetype="application/json",
            status_code=200,
        )

    except (ValueError, json.JSONDecodeError, IOError) as e:
        logging.exception("Error during ballot proofing.")
        return func.HttpResponse(f"Internal Server Error: {str(e)}", status_code=500)


@app.function_name(name="DefineBallot")
@app.route(route="define", methods=["POST"])
def define_ballot_api(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP triggered function to get a ballot definition."""

    logging.info("Define ballot triggered.")

    try:
        # Validate inputs
        file = req.files.get("file")
        pages = req.form.get("pages") or "1"

        if not file:
            return func.HttpResponse("Missing 'file' in form-data", status_code=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file.stream.read())
            ballot_path = tmp_file.name

        blob_url = save_to_blob_storage(ballot_path)
        logging.info("Ballot uploaded to blob storage: %s", blob_url)

        definition = get_definition(blob_url, pages=pages)

        return func.HttpResponse(
            {"definition": definition}, mimetype="application/json", status_code=200
        )

    except (ValueError, json.JSONDecodeError, IOError) as e:
        logging.exception("Error during ballot proofing.")
        return func.HttpResponse(f"Internal Server Error: {str(e)}", status_code=500)
