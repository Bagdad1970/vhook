from dataclasses import dataclass


@dataclass
class ChannelInfo:
    id: str
    title: str
    subscriber_count: int
    video_count: int
    playlist_id: str

    @classmethod
    def create_from_dict(cls, channel_info: dict):
        return cls(
            id=channel_info['id'],
            title=channel_info['snippet']['title'],
            subscriber_count=channel_info['statistics']['subscriberCount'],
            video_count=channel_info['statistics']['videoCount'],
            playlist_id=channel_info['contentDetails']['relatedPlaylists']['uploads']
        )