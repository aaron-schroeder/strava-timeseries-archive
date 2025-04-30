import json
import os
from pathlib import Path
from typing import List, Optional

from oauth.repository import AbstractAccessTokenRepository
from oauth.domain.model import AccessToken


class FileAccessTokenRepository(AbstractAccessTokenRepository):
    def __init__(self, directory):
        self.directory = directory

    def save(self, token) -> None:
        file_path = self._get_fname_by_id(token.athlete_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(token.to_dict(), f)

    def get(self, athlete_id) -> Optional[AccessToken]:
        file_path = self._get_fname_by_id(athlete_id)
        if not os.path.isfile(file_path):
            return None
        with open(self._get_fname_by_id(athlete_id), 'r') as f:
            token_data = json.load(f)
        return AccessToken.from_dict(token_data)
    
    def first(self) -> Optional[AccessToken]:
        try:
            first_json_filename = next(Path(self.directory).glob('*.json'))
        except StopIteration:
            return None
        with open(first_json_filename, 'r') as f:
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
