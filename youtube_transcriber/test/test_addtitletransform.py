from youtube_transcriber.transforming.addtitletransform import AddTitleTransform
from youtube_transcriber.video import YoutubeVideo

def test_whisper_transform_init():
    transform = AddTitleTransform()
    assert type(transform) == AddTitleTransform
    
def test_apply():
    transform = AddTitleTransform()
    raw_video = YoutubeVideo(channel_name="Tquotes",
                             url="https://www.youtube.com/watch?v=NSkoGZ8J1Ag")
    transformed_video = transform.apply(raw_video)
    assert type(transformed_video) == YoutubeVideo
    assert transformed_video.channel_name == raw_video.channel_name
    assert transformed_video.url == raw_video.url
    assert transformed_video.title == "Steve Jobs quotes Bob Dylan"
    assert transformed_video.description == raw_video.description
    assert transformed_video.transcription == raw_video.transcription
    assert transformed_video.segments == raw_video.segments