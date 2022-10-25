from youtube_transcriber.video import YoutubeVideo
from youtube_transcriber.utils import create_videos
from youtube_transcriber.utils import nest_list

def test_create_videos():
    video_params = [
        {'channel_name': 'MrBeast Shorts', 'url': 'https://www.youtube.com/watch?v=mJ4t7iNF86g'}, 
        {'channel_name': 'MrBeast Shorts', 'url': 'https://www.youtube.com/watch?v=UPhxU9J46Qk'}
    ]
    videos = create_videos(video_params)
    assert len(videos) == 2
    assert type(videos[0]) == YoutubeVideo
    assert videos[1].url == "https://www.youtube.com/watch?v=UPhxU9J46Qk"

def test_nest_list():
    l = [0, 1, 2, 3, 4, 5]
    
    nested_l = nest_list(l, 6)
    assert nested_l == [[0, 1, 2, 3, 4, 5]]
    
    nested_l = nest_list(l, 5)
    assert nested_l == [[0, 1, 2, 3, 4], [5]]
    
    nested_l = nest_list(l, 4)
    assert nested_l == [[0, 1, 2, 3], [4, 5]]
    
    nested_l = nest_list(l, 3)
    assert nested_l == [[0, 1, 2], [3, 4, 5]]
    
    nested_l = nest_list(l, 2)
    assert nested_l == [[0, 1], [2, 3], [4, 5]]
    
    nested_l = nest_list(l, 1)
    assert nested_l == [[0], [1], [2], [3], [4], [5]]