from pathlib import Path

import pytest

from youtube_transcriber.loading.loaderiterator import LoaderIterator
from youtube_transcriber.loading.serialization import JsonSerializer

@pytest.fixture
def loader_iterator():
    test_folder = Path.home()/"whisper_gpt_pipeline/youtube_transcriber/test"
    paths = [Path(test_folder/"files/1.json"), Path(test_folder/"files/2.json"), 
             Path("non-existing-path"), Path(test_folder/"files/3.json"), 
             Path(test_folder/"files/4.json"), Path(test_folder/"files/5.json")]
    return LoaderIterator(JsonSerializer(), 2, paths)

def test_loader_iterator_init():
    loader_iterator = LoaderIterator(JsonSerializer(), 3, "dummy_paths")
    assert type(loader_iterator) == LoaderIterator
    assert type(loader_iterator.serializer) == JsonSerializer
    assert loader_iterator.load_paths == "dummy_paths"
    assert loader_iterator.num_files_per_iteration == 3
    
def test_loop_through_loaded_data(loader_iterator):
    expected_data = [
        [
            {
                "channel_name": "The verge",
                "url": "https://www.youtube.com/watch?v=YMlTSmusEmA",
                "title": "Pixel 7 Pro and 7 hands-on: more of the same",
                "description": "Google’s Pixel 7 and 7 Pro..."
            },
            {
                "channel_name": "The verge",
                "url": "https://www.youtube.com/watch?v=Jzl0hHTc7Jw"
            }
        ],
        [
            {
                "channel_name": "The verge",
                "url": "https://www.youtube.com/watch?v=gV50hpSKHFQ"
            }
        ],
        [
            {
                "channel_name": "The verge",
                "url": "https://www.youtube.com/watch?v=N6ZyzoibXqg"
            },
            {
                "channel_name": "The verge",
                "url": "https://www.youtube.com/watch?v=q90v9FLXi1E"
            }
        ]
    ]
    
    for i, data in enumerate(loader_iterator):
        assert data == expected_data[i]