from flask_app import oauth_client
from flask_app.repository import FileAccessTokenRepository


def get_fresh_token(repo: FileAccessTokenRepository, athlete_id=None):
    if athlete_id is not None:
        token = repo.get(athlete_id)
    else:
        try:
            token = repo.find_all()[0]
        except IndexError:
            return None
    token = oauth_client.refresh(token)
    return token
