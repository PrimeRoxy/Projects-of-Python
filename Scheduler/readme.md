# Meeting Scheduler

The Meeting Scheduler is a Python script designed to streamline the process of scheduling meetings using the Google Calendar API. This script empowers users to efficiently plan their meetings, considering potential conflicts with existing appointments, and provides the flexibility to resolve conflicts gracefully.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed
- Google Calendar API credentials (client_secret.json)
- The required Python packages installed (`google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`, `pytz`)

## Set up the Google Calendar API:

# Follow the Google Calendar API Python Quickstart to generate credentials.json.
Authorize credentials for a desktop application
To authenticate as an end user and access user data in your app, you need to create one or more OAuth 2.0 Client IDs. A client ID is used to identify a single app to Google's OAuth servers. If your app runs on multiple platforms, you must create a separate client ID for each platform.
In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.
Go to Credentials

Click Create Credentials > OAuth client ID.
Click Application type > Desktop app.
In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
Save the downloaded JSON file as credentials.json, and move the file to your working directory.

Save credentials.json in the project directory