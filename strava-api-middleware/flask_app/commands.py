from oauth.domain.model import AccessToken, TrainingPeaksOAuthClient
from oauth.repository import AbstractAccessTokenRepository

from flask_app import oauth_client, tp_oauth_client


def get_fresh_token(repo: AbstractAccessTokenRepository, athlete_id=None) -> AccessToken:
    if athlete_id is not None:
        token = repo.get(athlete_id)
    else:
        token = repo.first()
    token = oauth_client.refresh(token)
    return token


def get_fresh_tp_token(repo: AbstractAccessTokenRepository, client: TrainingPeaksOAuthClient) -> AccessToken:
    token = repo.first()
    if token is None or token.is_expired:
        token = client.get_token()
    repo.save(token)
    return token
