import configparser
import pprint

import requests
from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from msal import PublicClientApplication

app = FastAPI()

# Create a ConfigParser instance
config = configparser.ConfigParser()

# Read the configuration file
config.read("config.cfg")

# Access variables in the [azure] section
CLIENT_ID = config.get("azure", "CLIENT_ID")
TENANT_ID = config.get("azure", "TENANT_ID")
SCOPE = config.get("azure", "SCOPE")
REDIRECT_URI = config.get("azure", "REDIRECT_URI")

# Define Microsoft Identity Platform authority URL
msal_authority = f"https://login.microsoftonline.com/{TENANT_ID}"
msal_scope = [SCOPE]

# Create a PublicClientApplication instance
msal_app = PublicClientApplication(
    client_id=CLIENT_ID, authority=msal_authority, redirect_uri=REDIRECT_URI
)


@app.get("/")
async def home():
    # Generate an authorization URL
    auth_url, state = msal_app.get_authorization_request_url(msal_scope)
    return {"Authorization URL": auth_url}


@app.get("/auth-callback/")
async def auth_callback(
    code: str = Query(..., description="Authorization code from Microsoft login")
):
    try:
        # Handle the callback and obtain the access token
        token_response = msal_app.acquire_token_by_authorization_code(
            code, scopes=msal_scope, redirect_uri=REDIRECT_URI
        )
        access_token = token_response.get("access_token")

        if access_token is None:
            raise HTTPException(status_code=400, detail="No Access Token Found")

        # Set the headers for making requests to the Microsoft Graph API
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Define the base URL for Microsoft Graph API and the endpoint for user information
        base_api: str = "https://graph.microsoft.com/v1.0"
        end_point: str = "me"

        # Make a GET request to the Microsoft Graph API to retrieve user information
        response = requests.get(url=f"{base_api}/{end_point}", headers=headers).json()

        # Return the user information
        return {"User Information": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
