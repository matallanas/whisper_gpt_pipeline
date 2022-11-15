from pathlib import Path
import pytest
import os

from youtube_transcriber.preprocessing.youtubevideopreprocessor import YoutubeVideoPreprocessor
from youtube_transcriber.loading.serialization import JsonSerializer

@pytest.fixture
def youtube_video_preprocessor():
    yt_video_preprocessor = YoutubeVideoPreprocessor(mode="channel_name",
                                                     serializer=JsonSerializer())
    load_paths, dataset_folder = yt_video_preprocessor.preprocess(name="Best Shorts Quotes",
                                                                  num_videos=2,
                                                                  videos_in_ds=["GU2_xlNCJrA"])
    return load_paths, dataset_folder

@pytest.fixture
def expected_file_paths():
    youtube_folder = Path.home()/"whisper_gpt_pipeline/youtube_transcriber"
    expected_dir = youtube_folder/"Best Shorts Quotes"
    return [expected_dir/"0.json", expected_dir/"1.json"]

@pytest.fixture
def expected_folder_path():
    youtube_folder = Path.home()/"whisper_gpt_pipeline/youtube_transcriber"
    expected_dir = youtube_folder/"Best Shorts Quotes"
    return expected_dir

def test_youtube_video_preprocessor_init():
    yt_video_preprocessor = YoutubeVideoPreprocessor(mode="channel_name",
                                                     serializer=JsonSerializer())
    assert type(yt_video_preprocessor) == YoutubeVideoPreprocessor
    assert type(yt_video_preprocessor.serializer) == JsonSerializer
    assert yt_video_preprocessor.mode == "channel_name"
    
def test_created_file(youtube_video_preprocessor, expected_file_paths):
    paths, _ = youtube_video_preprocessor
    for path in paths:
        assert os.path.exists(expected_file_paths[0]) == True
        assert os.path.exists(expected_file_paths[1]) == True

def test_created_folder(youtube_video_preprocessor, expected_folder_path):
    _, folder = youtube_video_preprocessor
    assert folder == expected_folder_path

def test_loop_through_created_files(youtube_video_preprocessor):
    expected_data = [
        {
            "channel_name": "Best Shorts Quotes",
            "url": "https://www.youtube.com/watch?v=GU2_xlNCJrA"
        },
        {
            "channel_name": "Best Shorts Quotes",
            "url": "https://www.youtube.com/watch?v=ttRI4EmmxkY"
        }
    ]

    paths, folder = youtube_video_preprocessor
    for i, path in enumerate(paths):
        serializer = JsonSerializer()
        assert serializer.load(path) == expected_data[i]