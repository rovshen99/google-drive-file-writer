# Django Google Drive Document Creation API

## Overview
This Django project provides an API to create documents on Google Drive. It's designed to receive document data via a POST request and then create a new document in Google's cloud storage.

## Features
- **Document Creation**: Users can send document data through an API request to create a new Google Doc.
- **Google OAuth2 Integration**: Utilizes Google's OAuth2 for authentication to access Google Drive.

## Requirements
- Python 3.x
- Django
- Google Cloud Platform account with Google Drive API enabled

## Installation
1. Clone the repository and navigate into the project directory.
2. Install required Python packages: `pip install -r requirements.txt`.
3. Set up Google Cloud Project:
   - Enable Google Drive API.
   - Create credentials (OAuth client ID and client secret).
   - Download the credentials JSON file.
4. Set environment variables for `GOOGLE_CREDS_PATH` (path to your Google credentials JSON) and `TOKEN_PATH` (path to save the token JSON).

## Usage
To create a document in Google Drive:
1. Send a POST request to `/google-drive/create-doc/` with the document's name and data in the request body.
2. Ensure the request includes appropriate headers for content type.

## API Endpoints
- **POST `/google-drive/create-doc/`**: Creates a new document in Google Drive with provided name and data.

## Configuration
- Configure the Google Drive API and OAuth2 credentials in the settings.
- Set the path for the credentials and token files in your environment variables.

## Troubleshooting
- Ensure the correct path for Google credentials and token in environment variables.
- Check for proper installation of all dependencies.
- Verify the Google Cloud project settings and API credentials.
