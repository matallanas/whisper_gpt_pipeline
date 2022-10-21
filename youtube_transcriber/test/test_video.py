import pytest

from youtube_transcriber.video import YoutubeVideo

def test_youtube_video_init():
    video = YoutubeVideo(channel_name="The verge",
                         url="https://www.youtube.com/watch?v=Jzl0hHTc7Jw",
                         title="Pixel 7 Pro and 7 hands-on: more of the same",
                         description="Google’s Pixel 7 and 7 Pro...",
                         transcription=" Seven years ago, we set out...",
                         segments=[{"start": 0.0, "end": 1.3, "text": " Seven years ago"},
                                   {"start": 1.3, "end": 2.3, "text": " we set out..."}])
    
    assert type(video) == YoutubeVideo
    assert video.channel_name == "The verge"
    assert video.url == "https://www.youtube.com/watch?v=Jzl0hHTc7Jw"
    assert video.title == "Pixel 7 Pro and 7 hands-on: more of the same"
    assert video.description == "Google’s Pixel 7 and 7 Pro..."
    assert video.transcription == " Seven years ago, we set out..."
    assert video.segments == [{"start": 0.0, "end": 1.3, "text": " Seven years ago"},
                              {"start": 1.3, "end": 2.3, "text": " we set out..."}]
    
def test_youtube_video_to_tuple():
    video = YoutubeVideo(channel_name="The verge",
                         url="https://www.youtube.com/watch?v=Jzl0hHTc7Jw",
                         title="Pixel 7 Pro and 7 hands-on: more of the same",
                         description="Google’s Pixel 7 and 7 Pro...",
                         transcription=" Seven years ago, we set out...",
                         segments=[{"start": 0.0, "end": 1.3, "text": " Seven years ago"},
                                   {"start": 1.3, "end": 2.3, "text": " we set out..."}])
    video_tuple = video.to_tuple()
    assert len(video_tuple) == 6
    assert type(video_tuple) == tuple
    assert video_tuple[0] == "The verge"
    assert video_tuple[1] == "https://www.youtube.com/watch?v=Jzl0hHTc7Jw"
    assert video_tuple[2] == "Pixel 7 Pro and 7 hands-on: more of the same"
    assert video_tuple[3] == "Google’s Pixel 7 and 7 Pro..."
    assert video_tuple[4] == " Seven years ago, we set out..."
    assert video_tuple[5] == [{"start": 0.0, "end": 1.3, "text": " Seven years ago"}, 
                              {"start": 1.3, "end": 2.3, "text": " we set out..."}]