from typing import Any

from pytube import YouTube

from youtube_transcriber.video import YoutubeVideo
from youtube_transcriber.utils import accepts_types
from youtube_transcriber.transforming.transform import Transform

class AddDescriptionTransform(Transform):
    """
    Transform a Video object using PyTube. Adds title to YouTube video DTO. 
    It's a concrete Transform.
    """
    
    @accepts_types(YoutubeVideo)
    def apply(self, video: YoutubeVideo) -> YoutubeVideo:
        
        yt = YouTube(video.url)
        
        video_With_description_params = {
            "channel_name": video.channel_name,
            "url": video.url,
            "title": video.title,
            "description": self._get_video_description(yt),
            "transcription": video.transcription,
            "segments": video.segments
        }
        
        return YoutubeVideo(**video_With_description_params)
    
    def _get_video_description(self, yt: Any) -> str:
        return str(yt.description)