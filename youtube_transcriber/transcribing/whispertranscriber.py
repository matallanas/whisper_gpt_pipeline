from youtube_transcriber.transcribing.transcribe import Transcribe
from youtube_transcriber.video import RawVideo, TranscribedVideo

class WhisperTranscriber(Transcribe):
    """
    Transcribe a Video object using Whisper model. It's a
    concrete Tranascriber.
    Args:
        model (`str`):
            Size of Whisper model. Can be tiny, base (default), small, medium, and large.
        without_timestamps (`bool`, defaults to `False`):
            To add phrase-level timestamps.
    """

    def __init__(self, model: str="base", without_timestamps: bool=False) -> None:
        self.model = model
        self.without_timestamps = without_timestamps

    def apply(self, raw_video: RawVideo) -> TranscribedVideo:
        """Creates a new video with transcriptions created by Whisper.
        """
        # TODO