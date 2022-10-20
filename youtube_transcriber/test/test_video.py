import pytest

from youtube_transcriber.video import RawVideo, TranscribedVideo

def test_raw_video_init():
    video = RawVideo(channel_name="The verge",
                     url="https://www.youtube.com/watch?v=YMlTSmusEmA",
                     title="Pixel 7 Pro and 7 hands-on: more of the same",
                     description="Google’s Pixel 7 and 7 Pro...")
    
    assert type(video) == RawVideo
    assert video.channel_name == "The verge"
    assert video.url == "https://www.youtube.com/watch?v=YMlTSmusEmA"
    assert video.title == "Pixel 7 Pro and 7 hands-on: more of the same"
    assert video.description == "Google’s Pixel 7 and 7 Pro..."
    
def test_raw_video_to_tuple():
    video = RawVideo(channel_name="The verge",
                     url="https://www.youtube.com/watch?v=YMlTSmusEmA",
                     title="Pixel 7 Pro and 7 hands-on: more of the same",
                     description="Google’s Pixel 7 and 7 Pro...")
    video_tuple = video.to_tuple()
    assert len(video_tuple) == 4
    assert type(video_tuple) == tuple
    assert video_tuple[0] == "The verge"
    assert video_tuple[1] == "https://www.youtube.com/watch?v=YMlTSmusEmA"
    assert video_tuple[2] == "Pixel 7 Pro and 7 hands-on: more of the same"
    assert video_tuple[3] == "Google’s Pixel 7 and 7 Pro..."
    
def test_transcribed_video_init():
    video = TranscribedVideo(channel_name="The verge",
                             url="https://www.youtube.com/watch?v=Jzl0hHTc7Jw",
                             title="Pixel 7 Pro and 7 hands-on: more of the same",
                             description="Google’s Pixel 7 and 7 Pro...",
                             transcription=" Seven years ago, we set out...",
                             segments=[{"start": 0.0, "end": 1.3, "text": " Seven years ago"},
                                       {"start": 1.3, "end": 2.3, "text": " we set out..."}])
    
    assert type(video) == TranscribedVideo
    assert video.channel_name == "The verge"
    assert video.url == "https://www.youtube.com/watch?v=Jzl0hHTc7Jw"
    assert video.title == "Pixel 7 Pro and 7 hands-on: more of the same"
    assert video.description == "Google’s Pixel 7 and 7 Pro..."
    assert video.transcription == " Seven years ago, we set out..."
    assert video.segments == [{"start": 0.0, "end": 1.3, "text": " Seven years ago"},
                              {"start": 1.3, "end": 2.3, "text": " we set out..."}]
    
def test_transcribed_video_to_tuple():
    video = TranscribedVideo(channel_name="The verge",
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