from dataclasses import dataclass
import datetime

import isodate

from src.utilities import create_youtube_url


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


@dataclass
class VideoInfo:
    id: str = ""
    title: str = ""
    published_at: datetime.date = None  # TODO is it datetime or just date ?
    duration: datetime.timedelta = datetime.timedelta(seconds=0)

    @classmethod
    def create_from_dict(cls, video_info: dict):
        id = video_info.get("id")

        title = video_info.get("title")

        published_at = None
        published_at_value =  video_info.get("published_at", "")
        if published_at_value:
            published_at = datetime.datetime.fromisoformat(published_at_value).date()

        duration = datetime.timedelta(seconds=0)
        duration_value = video_info.get("duration", "")
        if duration_value:
            duration = isodate.parse_duration(duration_value)

        return cls(
            id=id,
            title=title,
            published_at=published_at,  # TODO check format from youtube-api
            duration=duration,
        )

    def print_all(self):
        print(f"""url={create_youtube_url(self.id)} title={self.title!r} published_at={self.published_at!r} duration={self.duration!r}""")

@dataclass
class VideoQuery:
    search_pattern: str = ""
    from_date: datetime.date = datetime.date(1, 1, 1)
    to_date: datetime.date = datetime.date(9999, 12, 31)
    min_duration: datetime.timedelta = None
    max_duration: datetime.timedelta = None

    def matches(self, video_info: VideoInfo) -> bool:
        if self.search_pattern:
            if self.search_pattern.lower() not in video_info.title.lower():
                return False

        if not (self.from_date <= video_info.published_at <= self.to_date):
            return False

        if video_info.duration is not None:
            if self.min_duration is not None and video_info.duration < self.min_duration:
                return False
            if self.max_duration is not None and video_info.duration > self.max_duration:
                return False

        return True
