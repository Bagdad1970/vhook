from src.constant import YOUTUBE_URL_PREFIX


VALID_EXTENSIONS = ["mp4", "m4a", "webm", "mp3"]

def create_youtube_url(video_info: dict):
    return f'{YOUTUBE_URL_PREFIX}{video_info["video_id"]}'