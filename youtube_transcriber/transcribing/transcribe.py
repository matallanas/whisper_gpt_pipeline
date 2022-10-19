from abc import ABC, abstractmethod

from youtube_transcriber.video import RawVideo, TranscribedVideo


class Transcribe(ABC):
    """Interface for concrete Transcribe which transcribes a video object."""

    @abstractmethod
    def apply(self, product: RawVideo) -> TranscribedVideo:
        """Apply a transcription to a video. Method must be implemented by
        concrete transcribers."""