from abc import ABC, abstractmethod

from youtube_transcriber.video import YoutubeVideo

class Transform(ABC):
    """Interface for concrete Transform which transform a video object."""

    @abstractmethod
    def apply(self, video: YoutubeVideo) -> YoutubeVideo:
        """Apply a transform to a video. Method must be implemented by
        concrete transforms."""