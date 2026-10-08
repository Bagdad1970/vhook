from dataclasses import dataclass

import datetime

from src.models.video_info import VideoInfo


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
