import pytest

from youtube_transcriber.transforming.addtitletransform import AddTitleTransform
from youtube_transcriber.transforming.adddescriptiontransform import AddDescriptionTransform
from youtube_transcriber.transforming.batchtransformer import BatchTransformer
from youtube_transcriber.transforming.whispertransform import WhisperTransform
from youtube_transcriber.video import YoutubeVideo

@pytest.fixture
def batch_transformer():
    add_title_transform = AddTitleTransform()
    add_description_transform = AddDescriptionTransform()
    whisper_transform = WhisperTransform()
    return BatchTransformer([add_title_transform,
                             add_description_transform,
                             whisper_transform])

def test_batch_transform_init(batch_transformer):
    assert type(batch_transformer) == BatchTransformer
    assert len(batch_transformer.transforms) == 3
    assert type(batch_transformer.transforms[2]) == WhisperTransform

def test_apply_transforms(batch_transformer):
    videos = [YoutubeVideo(channel_name="Tquotes",
                           url="https://www.youtube.com/watch?v=NSkoGZ8J1Ag"),
              YoutubeVideo(channel_name="changminjen",
                           url="https://www.youtube.com/watch?v=Ak516vtDTEA")]
    transformed_videos = batch_transformer.apply(videos)
    assert len(transformed_videos) == 2
    assert transformed_videos[0].channel_name == "Tquotes"
    assert transformed_videos[0].url == "https://www.youtube.com/watch?v=NSkoGZ8J1Ag"
    assert transformed_videos[0].title == "Steve Jobs quotes Bob Dylan"
    assert transformed_videos[0].description == ""
    assert transformed_videos[0].transcription == " Good morning. Good morning and welcome to Apple's 1984 annual shareholders meeting. I'd like to open the meeting with a part of an old poem about a 20-year-old poem by Dylan. That's Bob Dylan. Come writers and critics who prophesize with your pens and keep your eyes wide, the chance won't come again. And don't speak too soon for the wheels still in spin. And there's no telling who that it's naming. For the loser now will be later to win for the times they are a change in. Now."
    assert transformed_videos[0].segments == [{'start': 0.0, 'end': 2.0, 'text': ' Good morning.'},
                                              {'start': 2.0, 'end': 11.0, 'text': " Good morning and welcome to Apple's 1984 annual shareholders meeting."},
                                              {'start': 11.0, 'end': 16.0, 'text': " I'd like to open the meeting with a part of an old poem about a 20-year-old poem by Dylan."},
                                              {'start': 16.0, 'end': 18.0, 'text': " That's Bob Dylan."},
                                              {'start': 18.0, 'end': 23.0, 'text': ' Come writers and critics who prophesize with your pens and keep your eyes wide,'},
                                              {'start': 23.0, 'end': 25.0, 'text': " the chance won't come again."},
                                              {'start': 25.0, 'end': 28.0, 'text': " And don't speak too soon for the wheels still in spin."},
                                              {'start': 28.0, 'end': 30.0, 'text': " And there's no telling who that it's naming."},
                                              {'start': 30.0, 'end': 36.0, 'text': ' For the loser now will be later to win for the times they are a change in.'},
                                              {'start': 36.0, 'end': 51.0, 'text': ' Now.'}]
    assert transformed_videos[1].channel_name == "changminjen"
    assert transformed_videos[1].url == "https://www.youtube.com/watch?v=Ak516vtDTEA"
    assert transformed_videos[1].title == "My allegiance is to the Republic, to democracy!"
    assert transformed_videos[1].description == "Anakin, my allegiance is to the Republic, to democracy! from Star Wars Episode III: Revenge of the Sith."
    assert transformed_videos[1].transcription == " I have brought peace, freedom, justice and security to my new empire. Your new empire don't make me kill you. Anakin, my allegiance is to the Republic, to democracy! If you're not with me, then you're my enemy. Only a Sith deals an absolute."
    assert transformed_videos[1].segments == [{'start': 0.0, 'end': 8.0, 'text': ' I have brought peace, freedom, justice and security to my new empire.'},
                                              {'start': 8.0, 'end': 14.0, 'text': " Your new empire don't make me kill you."},
                                              {'start': 14.0, 'end': 20.0, 'text': ' Anakin, my allegiance is to the Republic, to democracy!'},
                                              {'start': 20.0, 'end': 26.0, 'text': " If you're not with me, then you're my enemy."},
                                              {'start': 26.0, 'end': 31.0, 'text': ' Only a Sith deals an absolute.'}]