import os

from oauth.domain.model import OAuthClient
from ratelimit.domain.model import RateLimit

from .repository import FileAccessTokenRepository


repo = FileAccessTokenRepository(
    os.getenv('STRAVA_OAUTH_TOKEN_STORAGE_DIR')
)

oauth_client = OAuthClient(
    client_id=os.getenv('STRAVA_OAUTH_CLIENT_ID'),
    client_secret=os.getenv('STRAVA_OAUTH_CLIENT_SECRET')
)

rate_limit = RateLimit()