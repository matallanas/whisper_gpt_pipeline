import json
from typing import Any

VIDEO_INFO = [
              "id",
              "channel",
              "channel_id",
              "title",
              "categories",
              "tags",
              "description"
            ]

TRANSCRIPT_INFO = ["text", "segments"]

SEGMENTS_INFO = ["start", "end", "text"]

AUDIO_FILES = [".webm", ".mp3", ".flac", ".wav", ".m4a"]

AUDIO_FEATURE = "audio"

YT_OPTIONS = {
              "format": "bestaudio/best",
              "extractaudio": True,
              "audioformat": "mp3",
              "yesplaylist": True,
              "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
              }],
              "ignoreerrors": True
            }


def json_dump(obj: Any, save_path: str) -> None:
  with open(save_path, "w") as file:
    json.dump(obj, file)
