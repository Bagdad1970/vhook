import yt_dlp
from googleapiclient.discovery import build

import src.constant as constant
from src.format_info_container import FormatInfoContainer
from src.models.channel import VideoQuery, VideoInfo, ChannelInfo
from src.models.format_info import Format
from src.providers.abstract_provider import AbstractProvider


class YoutubeProvider(AbstractProvider):
    SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self._request_builder = build(serviceName=self.SERVICE_NAME, version=self.API_VERSION, developerKey=self._api_key)


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


    def find_channel(self, name: str):
        if not name.startswith('@'):
            name = '@' + name

        response = self._request_builder.channels().list(
            part='snippet,contentDetails,statistics',
            forHandle=name
        ).execute()

        if not response['items']:
            print(f'Channel "{name}" not found.')
            return None

        channel_info = response['items'][0]
        return ChannelInfo.create_from_dict(channel_info)


    @staticmethod
    def filter_videos_from_channel_by_query(video_infos: list[VideoInfo], query: VideoQuery) -> list:
        if not video_infos or query is None:
            return []

        return list(filter(query.matches, video_infos))


    def find_videos_by_query(self, channel: ChannelInfo, query=None):
        videos = []
        next_page_token = None

        while True:
            playlist_response = self._request_builder.playlistItems().list(
                part='snippet',
                playlistId=channel.playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            batch_ids = []
            batch_items = []
            for item in playlist_response['items']:
                # TODO firstly use title, id and published_at to filter batch
                # then use next fields

                video_info_dict = {
                    'title': item['snippet']['title'],
                    'id': item['snippet']['resourceId']['videoId'],
                    'published_at': item['snippet']['publishedAt']
                }

                batch_items.append(video_info_dict)
                batch_ids.append(video_info_dict.get('id'))

            if batch_ids:
                details_response = self._request_builder.videos().list(
                    part='contentDetails,snippet,statistics',
                    id=','.join(batch_ids)
                ).execute()

                details_by_id = { video_info_dict['id']: video_info_dict for video_info_dict in details_response['items'] }
                for video_info_dict in batch_items:
                    detail = details_by_id.get(video_info_dict.get('id'), {})
                    video_info_dict['duration'] = detail.get('contentDetails', {}).get('duration')

            video_infos = []
            for video_info_dict in batch_items:
                video_infos.append(VideoInfo.create_from_dict(video_info_dict))

            if query is not None:
                videos.extend(self.filter_videos_from_channel_by_query(video_infos, query))
            else:
                videos.extend(video_infos)

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break

        return videos