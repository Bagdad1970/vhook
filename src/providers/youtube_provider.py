import yt_dlp
from googleapiclient.discovery import build

from src.format_info_container import FormatInfoContainer
from src.models.format_info import Format
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

    def get_formats(self, url: str):
        opts = {
            # TODO cookies must be paramatrized
            "cookiesfrombrowser": ("firefox",),
            "js_runtimes": {
                # TODO must use deno lib
                "deno": {
                    "path": "/home/bagdad/.deno/bin/deno"
                }
            },
            "remote_components": ["ejs:github"],
            "quiet": False,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)

        format_infos = []
        for format_info in info['formats']:
            format_infos.append(Format.create_from_dict(format_info))

        valid_format_infos = []
        for format_info in format_infos:
            if format_info.is_valid():
                valid_format_infos.append(format_info)

        return FormatInfoContainer(valid_format_infos)