import json
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

class YoutubeVideo(BaseModel):
    """This class represent a YouTube video entry
    """
    channel_name: str
    url: str
    title: Optional[str]
    description: Optional[str]
    transcription: Optional[str]
    segments: Optional[List[Dict]] = None
    
    def to_tuple(self) -> Tuple:
        """Convert TranscribedVideo object to a tuple of the type:
        (channel_name, url, title, description, transcription, segments).
        """
        return (self.channel_name, self.url, self.title,
                self.description, self.transcription, self.segments)