import json

from django.http import JsonResponse
import os
import logging

from django.views.decorators.http import require_http_methods
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

logger = logging.getLogger(__name__)
SCOPES = ["https://www.googleapis.com/auth/drive"]


@require_http_methods(["POST"])
def create_google_doc(request):
    try:
        # Retrieve and validate input data
        data = json.loads(request.body)
        file_name, file_data = data.get("name"), data.get("data")
        # Return an error response if either file name or data is missing
        if not file_name or not file_data:
            return JsonResponse(
                {"status": "error", "message": "Invalid input"}, status=400
            )

        # Load credentials from the specified path in environment variables
        creds = None
        if os.path.exists(os.getenv("TOKEN_PATH")):
            creds = Credentials.from_authorized_user_file(
                os.getenv("TOKEN_PATH"), SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.getenv("GOOGLE_CREDS_PATH"), SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        # Initialize the Google Drive API service
        service = build("drive", "v3", credentials=creds)

        # Create the file metadata and upload media
        file_metadata = {
            "name": file_name,
            "mimeType": "application/vnd.google-apps.document",
        }
        media = MediaIoBaseUpload(io.BytesIO(file_data.encode()), mimetype="text/plain")
        # Create the file on Google Drive
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        # Return a success response with the created file's ID
        return JsonResponse({"status": "success", "file_id": file.get("id")})
    except Exception as e:
        # Log any exceptions that occur and return an error response
        logger.error(f"Error while creating a document: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
