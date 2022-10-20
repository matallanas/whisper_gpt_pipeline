import os
from pathlib import Path

from pytube import YouTube
import whisper

from youtube_transcriber.transcribing.transcribe import Transcriber
from youtube_transcriber.video import RawVideo, TranscribedVideo

class WhisperTranscriber(Transcriber):
    """
    Transcribe a Video object using Whisper model. It's a
    concrete Transcriber.
    Args:
        model (`str`):
            Size of Whisper model. Can be tiny, base (default), small, medium, and large.
        without_timestamps (`bool`, defaults to `False`):
            To add phrase-level timestamps.
    """

    def __init__(self, model: str="base", without_timestamps: bool=False) -> None:
        self.model = whisper.load_model(model)
        self.without_timestamps = without_timestamps

    def apply(self, raw_video: RawVideo) -> TranscribedVideo:
        """Creates a new video with transcriptions created by Whisper.
        """
        # Get audio from video
        try:
            audio_file = self._get_audio_from_video(raw_video)
        
        except Exception as e:
            print(f"Exception: {e}")
        
        result = self.model.transcribe(audio_file, 
                                       without_timestamps=self.without_timestamps)
        transcription = result["text"]
        
        data = []
        for seg in result['segments']:
            data.append({'start': seg['start'], 'end': seg['end'],'text': seg['text']})

        os.remove(audio_file)

        return TranscribedVideo(channel_name = RawVideo.channel_name,
                                url = RawVideo.url,
                                title = RawVideo.title,
                                description = RawVideo.title,
                                transcription = transcription,
                                segments = data)
        
    def _get_audio_from_video(self, raw_video: RawVideo) -> Path:
        # TODO: Add credits
        yt = YouTube(raw_video.url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=".")
        base, _ = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)
        return new_file