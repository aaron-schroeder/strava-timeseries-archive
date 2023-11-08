import json
import os
from pathlib import Path
from typing import List

from oauth.repository import AbstractAccessTokenRepository
from oauth.domain.model import AccessToken


class FileAccessTokenRepository(AbstractAccessTokenRepository):
    def __init__(self, directory):
        self.directory = directory

    def save(self, token) -> None:
        with open(self._get_fname_by_id(token.athlete_id), 'w') as f:
            json.dump(token.to_dict(), f)

    def get(self, athlete_id) -> AccessToken:
        with open(self._get_fname_by_id(athlete_id), 'r') as f:
            token_data = json.load(f)
        return AccessToken.from_dict(token_data)
    
    def find_all(self) -> List[AccessToken]:
        res = []
        for file_path in Path(self.directory).glob('*.json'):
            with open(file_path, 'r') as f:
                token_data = json.load(f)
            res.append(AccessToken.from_dict(token_data))
        return res
    
    def _get_fname_by_id(self, athlete_id):
        return os.path.join(self.directory, f'{athlete_id}.json')
