import yt_dlp
from googleapiclient.discovery import build

from src.providers.abstract_provider import AbstractProvider
import src.constant as constant


class YoutubeProvider(AbstractProvider):
    SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.request_builder = build(serviceName=self.SERVICE_NAME, version=self.API_VERSION, developerKey=self._api_key)

    def download_by_url(self, url: str, user_options: dict):
        options = constant.YOUTUBE_YT_DLP_OPTIONS | user_options

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([ url ])
