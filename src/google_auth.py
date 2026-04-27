import os

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")


def verify_google_token(token: str):
    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        return {
            "email": idinfo["email"],
            "name": idinfo.get("name")
        }

    except Exception:
        return None