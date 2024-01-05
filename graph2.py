import asyncio
import json
import os

from msal import PublicClientApplication

# MSAL configuration
msal_config = {
    "authority": "https://login.microsoftonline.com/218da14f-b67f-4503-b451-7bcad1d43d3f",
    "client_id": "8f10dacd-ec49-44e3-8a6a-1859e7347ba1",
}

# Scopes for the MSAL request
msal_scopes = []


def ensure_scope(scope):
    if scope.lower() not in (s.lower() for s in msal_scopes):
        msal_scopes.append(scope)


# Initialize MSAL client
msal_client = PublicClientApplication(
    client_id=msal_config["client_id"],
    authority=msal_config["authority"],
)


# Function to sign in the user
def sign_in():
    # Since MSAL Python doesn't support loginPopup, we'll have to use acquire_token_interactive
    result = msal_client.acquire_token_interactive(scopes=msal_scopes)
    if "account" in result:
        account = result["account"]
        with open("session.json", "w") as session_file:
            json.dump({"msalAccount": account.username}, session_file)


# Function to get token from Graph
async def get_token():
    try:
        with open("session.json", "r") as session_file:
            session_info = json.load(session_file)
            accounts = msal_client.get_accounts()
            user_account = next(
                (
                    acc
                    for acc in accounts
                    if acc.username == session_info.get("msalAccount")
                ),
                None,
            )

            if user_account is None:
                raise Exception(
                    "User info cleared from session. Please sign out and sign in again."
                )

        # First, attempt to get the token silently
        silent_result = msal_client.acquire_token_silent(
            scopes=msal_scopes, account=accounts[0]
        )
        if silent_result:
            return silent_result["access_token"]

        # If silent request fails, attempt to get the token interactively
        interactive_result = msal_client.acquire_token_interactive(scopes=msal_scopes)
        access_token = interactive_result["access_token"]
        print("Access Token (Interactive):", access_token)
        return access_token

    except Exception as e:
        # Handle any other exceptions
        raise e


async def main():
    sign_in()  # Uncomment this if you need to perform sign in
    await get_token()


# Run the main function
asyncio.run(main())
