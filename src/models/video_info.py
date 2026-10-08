from dataclasses import dataclass

import datetime

import isodate

from src.utilities import create_youtube_url


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
