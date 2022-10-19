from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

class RawVideo(BaseModel):
    """
    This class represent a video entry before transcription
    """
    channel_name: str
    url: str
    
    # TODO: Add URL validator

    def to_tuple(self) -> Tuple:
        """Convert RawVideo object to a tuple of the type:
        (channel_name, url).
        """
        return (self.channel_name, self.url)

class TranscribedVideo(BaseModel):
    """This class represent a video entry after transcription
    """
    channel_name: str
    url: str
    transcription: str
    segments: Optional[List[Dict]] = None
    
    def to_tuple(self) -> Tuple:
        """Convert TranscribedVideo object to a tuple of the type:
        (channel_name, url).
        """
        return (self.channel_name, self.url, 
                self.transcription, self.segments)