from youtube_transcriber.video import YoutubeVideo
from youtube_transcriber.utils import create_videos

def test_create_videos():
    video_params = [
        {'channel_name': 'MrBeast Shorts', 'url': 'https://www.youtube.com/watch?v=mJ4t7iNF86g'}, 
        {'channel_name': 'MrBeast Shorts', 'url': 'https://www.youtube.com/watch?v=UPhxU9J46Qk'}
    ]
    videos = create_videos(video_params)
    assert len(videos) == 2
    assert type(videos[0]) == YoutubeVideo
    assert videos[1].url == "https://www.youtube.com/watch?v=UPhxU9J46Qk"