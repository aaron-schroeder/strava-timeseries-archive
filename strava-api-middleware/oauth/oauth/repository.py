import abc
from oauth.domain.model import AccessToken


class AbstractAccessTokenRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, token: AccessToken) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, athlete_id: int) -> AccessToken:
        raise NotImplementedError