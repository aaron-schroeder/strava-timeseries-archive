from dataclasses import dataclass
import datetime
from urllib.parse import urlencode, urlparse

import requests


class ValueObject:
    pass


class Entity:
    pass


@dataclass
class AccessTokenObject(ValueObject):
    bearer_token: str
    refresh_token: str
    expires_at: int

    @classmethod
    def from_dict(cls, token_data):
        return cls(bearer_token=token_data['access_token'],
                   refresh_token=token_data['refresh_token'],
                   expires_at=token_data['expires_at'])

    @property
    def is_expired(self):
        return datetime.datetime.utcnow() > self.expiration_time

    @property
    def expiration_time(self):
        return datetime.datetime.utcfromtimestamp(self.expires_at)

    def to_dict(self):
        return dict(
            access_token=self.bearer_token, 
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
            expiration_time=str(self.expiration_time)  # convenience
        )


@dataclass
class AccessToken(Entity):
    athlete_id: int
    access_token_object: AccessTokenObject
  
    @classmethod
    def from_dict(cls, token_data):
        athlete_data = token_data.get('athlete')
        assert athlete_data is not None
        access_token_object = AccessTokenObject.from_dict(token_data)
        return cls(athlete_id=athlete_data['id'], 
                   access_token_object=access_token_object)

    def get_bearer_token(self):
        return self.access_token_object.bearer_token
    
    def get_refresh_token(self):
        return self.access_token_object.refresh_token

    def to_dict(self):
        return dict(athlete=dict(id=self.athlete_id), 
                    **self.access_token_object.to_dict())
    

class OAuthClient:
    def __init__(self, client_id: int, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def generate_auth_url(self, redirect_url):
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'scope': 'activity:read_all', 
                  'redirect_uri': redirect_url,
                  'approval_prompt': 'auto'}
        query = urlencode(params)
        return 'https://www.strava.com/oauth/authorize?' + query

    def exchange_for_token(self, code: str) -> AccessToken:
        resp = requests.post('https://www.strava.com/api/v3/oauth/token',
                             data={'grant_type': 'authorization_code', 
                                   'code': code,
                                   'client_id': self.client_id,
                                   'client_secret': self.client_secret})
        assert resp.status_code == 200
        token_data = resp.json()
        return AccessToken.from_dict(token_data)

    def refresh(self, access_token: AccessToken):
        resp = requests.post(
            'https://www.strava.com/api/v3/oauth/token', 
            data={'grant_type': 'refresh_token',
                  'refresh_token': access_token.get_refresh_token(),
                  'client_id': self.client_id,
                  'client_secret': self.client_secret})
        assert resp.status_code == 200
        data = resp.json()
        access_token.access_token_object = AccessTokenObject.from_dict(data)
        return access_token
    

# class AuthenticatedHttpClient:
#     def __init__(self, token: AccessToken):
#         self.token = token
class ResourceHttpClient:
    def __init__(self, token: AccessToken):
        self.token = token

    def get(self, url, params={}):
        auth_header = {
            'authorization': 'Bearer ' + self.token.get_bearer_token()
        }
        response = requests.get(url, headers=auth_header, params=params)
        return response