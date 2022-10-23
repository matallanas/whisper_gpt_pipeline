from pathlib import Path
import pytest
import os

from youtube_transcriber.preprocessing.youtubevideopreprocessor import YoutubeVideoPreprocessor
from youtube_transcriber.loading.serialization import JsonSerializer

@pytest.fixture
def youtube_video_preprocessor():
    yt_video_preprocessor = YoutubeVideoPreprocessor(mode="channel_name",
                                                     serializer=JsonSerializer())
    load_paths = yt_video_preprocessor.preprocess(name="Best Shorts Quotes",
                                                  num_videos=2)
    return load_paths

@pytest.fixture
def expected_file_paths():
    youtube_folder = Path.home()/"whisper_gpt_pipeline/youtube_transcriber"
    expected_dir = youtube_folder/"Best Shorts Quotes"
    return [expected_dir/"0.json", expected_dir/"1.json"]

def test_youtube_video_preprocessor_init():
    yt_video_preprocessor = YoutubeVideoPreprocessor(mode="channel_name",
                                                     serializer=JsonSerializer())
    assert type(yt_video_preprocessor) == YoutubeVideoPreprocessor
    assert type(yt_video_preprocessor.serializer) == JsonSerializer
    assert yt_video_preprocessor.mode == "channel_name"
    
def test_created_file(youtube_video_preprocessor, expected_file_paths):
    for path in youtube_video_preprocessor:
        assert os.path.exists(expected_file_paths[0]) == True
        assert os.path.exists(expected_file_paths[1]) == True