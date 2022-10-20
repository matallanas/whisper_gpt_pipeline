import os
from pathlib import Path
from typing import Any

from pytube import YouTube
import whisper

from youtube_transcriber.transcribing.transcribe import Transcriber
from youtube_transcriber.video import RawVideo, TranscribedVideo
from youtube_transcriber.utils import accepts_types

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

    @accepts_types(RawVideo) 
    def apply(self, raw_video: RawVideo) -> TranscribedVideo:
        """Creates a new video with transcriptions created by Whisper.
        """
        # Create a YouTube object
        yt = YouTube(raw_video.url)
        
        # Get audio from video
        try:
            audio_file = self._get_audio_from_video(yt)
        
        except Exception as e:
            print(f"Exception: {e}")
        
        result = self.model.transcribe(audio_file, 
                                       without_timestamps=self.without_timestamps)
        transcription = result["text"]
        
        data = []
        for seg in result['segments']:
            data.append({'start': seg['start'], 'end': seg['end'],'text': seg['text']})

        os.remove(audio_file)

        return TranscribedVideo(channel_name = raw_video.channel_name,
                                url = raw_video.url,
                                title = self._get_video_title(yt),
                                description = self._get_video_description(yt),
                                transcription = transcription,
                                segments = data)
        
    def _get_audio_from_video(self, yt: Any) -> Path:
        # TODO: Add credits
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=".")
        base, _ = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)
        return new_file
    
    def _get_video_title(self, yt: Any) -> str:
        return str(yt.title)
    
    def _get_video_description(self, yt: Any) -> str:
        return str(yt.description)