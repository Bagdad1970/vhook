import yt_dlp
from googleapiclient.discovery import build

import core.constant as constant
from core.format_info_container import FormatInfoContainer
from core.models import VideoInfo, ChannelInfo, VideoQuery
from core.models.format_info import FormatInfo
from core.providers.abstract_provider import AbstractProvider


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
            format_infos.append(FormatInfo.create_from_dict(format_info))

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
        return ChannelInfo.from_dict(channel_info)


    def find_videos_by_query(self, channel: ChannelInfo, query: VideoQuery=None):
        videos = []
        next_page_token = None

        while True:
            playlist_response = self._request_builder.playlistItems().list(
                part='snippet',
                playlistId=channel.playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            batch_video_info_dicts = []
            batch_video_ids = []
            for item in playlist_response['items']:
                video_info_dict = {
                    'id': item['snippet']['resourceId']['videoId'],
                    'title': item['snippet']['title'],
                    'published_at': item['snippet']['publishedAt']
                }

                batch_video_info_dicts.append(video_info_dict)
                batch_video_ids.append(video_info_dict['id'])

            self._add_video_details(video_ids=batch_video_ids, video_info_dicts=batch_video_info_dicts)

            video_infos = [ VideoInfo.from_dict(video_info_dict) for video_info_dict in batch_video_info_dicts ]

            filtered_video_infos = [ video_info for video_info in video_infos if query.matches(video_info) ]

            videos.extend(filtered_video_infos)

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break

        return videos


    def _add_video_details(self, video_ids: list, video_info_dicts: list):
        if not video_ids:
            return

        details_response = self._request_builder.videos().list(
            part='contentDetails,snippet,statistics',
            id=','.join(video_ids)
        ).execute()

        details_by_id = { video_info_dict['id']: video_info_dict for video_info_dict in details_response['items'] }
        for video_info_dict in video_info_dicts:
            detail = details_by_id.get(video_info_dict.get('id'), {})
            video_info_dict['duration'] = detail.get('contentDetails', {}).get('duration')