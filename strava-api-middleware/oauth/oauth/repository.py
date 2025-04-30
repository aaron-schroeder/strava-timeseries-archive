import abc
from typing import Optional

from oauth.domain.model import AccessToken


class AbstractAccessTokenRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, token: AccessToken) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, athlete_id: int) -> Optional[AccessToken]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def first(self, athlete_id: int) -> Optional[AccessToken]:
        raise NotImplementedError