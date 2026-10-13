from abc import ABC, abstractmethod


class AbstractProvider(ABC):

    def __init__(self, api_key):
        self._api_key = api_key

    @abstractmethod
    def download_by_url(self, url: str, user_options: dict):
        pass

    @abstractmethod
    def get_formats(self, url: str):
        pass