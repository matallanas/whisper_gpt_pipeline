from youtube_transcriber.transforming.adddescriptiontransform import AddDescriptionTransform
from youtube_transcriber.video import YoutubeVideo

def test_add_description_transform_init():
    transform = AddDescriptionTransform()
    assert type(transform) == AddDescriptionTransform
    
def test_apply():
    transform = AddDescriptionTransform()
    raw_video = YoutubeVideo(channel_name="changminjen",
                             url="https://www.youtube.com/watch?v=Ak516vtDTEA")
    transformed_video = transform.apply(raw_video)
    assert type(transformed_video) == YoutubeVideo
    assert transformed_video.channel_name == raw_video.channel_name
    assert transformed_video.url == raw_video.url
    assert transformed_video.title == raw_video.title
    assert transformed_video.description == "Anakin, my allegiance is to the Republic, to democracy! from Star Wars Episode III: Revenge of the Sith."
    assert transformed_video.transcription == raw_video.transcription
    assert transformed_video.segments == raw_video.segments