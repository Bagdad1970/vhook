from pydantic import BaseModel, Field, DirectoryPath


class YoutubeBaseQuery(BaseModel):
    quality: str = Field(default="", description="Which video quality to prefer")
    write_thumbnail: bool = Field(False, description="Whether to write thumbnail of video")
    download_dir: DirectoryPath = Field(..., description="Directory to download videos")


class YoutubeChannelQuery(YoutubeBaseQuery):
    channel_id: str = Field(..., description="YouTube channel ID")


class YoutubeUrlQuery(YoutubeBaseQuery):
    url: str = Field(..., description="YouTube video url")
