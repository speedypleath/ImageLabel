
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [  'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/cloud-vision',
            "https://www.googleapis.com/auth/photoslibrary"]


def google_auth():
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file='client_secrets.json',
        scopes=SCOPES, redirect_uri = "http://localhost:8080")
    auth_uri = flow.authorization_url()
    cred = flow.run_local_server(
        host='localhost',
        port=8080,
        open_browser=True,)
    """
    din cred trebuie salvate token si refresh_token pentru a putea accesa celelalte api-uri
    """
    session = flow.authorized_session()
    profile_info = session.get(
    'https://www.googleapis.com/userinfo/v2/me').json()

    print(profile_info)
    """
    in profile_info sunt informatii care pot sa se adauge la profilul utilizatorului
    """
    profile_info["token"] = cred.token
    profile_info["refresh_token"] = cred.refresh_token
    return profile_info