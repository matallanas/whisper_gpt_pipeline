from youtube_transcriber.transforming.whispertransform import WhisperTransform
from youtube_transcriber.video import YoutubeVideo

def test_whisper_transform_init():
    transcriber = WhisperTransform()
    assert type(transcriber) == WhisperTransform
    # TODO: Check if loaded model is 'base'
    assert transcriber.without_timestamps == False
    
def test_apply():
    transcriber = WhisperTransform()
    raw_video = YoutubeVideo(channel_name="Tquotes",
                             url="https://www.youtube.com/watch?v=NSkoGZ8J1Ag")
    transcribed_video = transcriber.apply(raw_video)
    assert type(transcribed_video) == YoutubeVideo
    assert transcribed_video.channel_name == raw_video.channel_name
    assert transcribed_video.url == raw_video.url
    assert transcribed_video.title == raw_video.title
    assert transcribed_video.description == raw_video.description
    assert transcribed_video.transcription == " Good morning. Good morning and welcome to Apple's 1984 annual shareholders meeting. I'd like to open the meeting with a part of an old poem about a 20-year-old poem by Dylan. That's Bob Dylan. Come writers and critics who prophesize with your pens and keep your eyes wide, the chance won't come again. And don't speak too soon for the wheels still in spin. And there's no telling who that it's naming. For the loser now will be later to win for the times they are a change in. Now."
    assert transcribed_video.segments == [{'start': 0.0, 'end': 2.0, 'text': ' Good morning.'}, 
                                          {'start': 2.0, 'end': 11.0, 'text': " Good morning and welcome to Apple's 1984 annual shareholders meeting."}, 
                                          {'start': 11.0, 'end': 16.0, 'text': " I'd like to open the meeting with a part of an old poem about a 20-year-old poem by Dylan."}, 
                                          {'start': 16.0, 'end': 18.0, 'text': " That's Bob Dylan."}, 
                                          {'start': 18.0, 'end': 23.0, 'text': ' Come writers and critics who prophesize with your pens and keep your eyes wide,'}, 
                                          {'start': 23.0, 'end': 25.0, 'text': " the chance won't come again."}, 
                                          {'start': 25.0, 'end': 28.0, 'text': " And don't speak too soon for the wheels still in spin."}, 
                                          {'start': 28.0, 'end': 30.0, 'text': " And there's no telling who that it's naming."}, 
                                          {'start': 30.0, 'end': 36.0, 'text': ' For the loser now will be later to win for the times they are a change in.'}, 
                                          {'start': 36.0, 'end': 51.0, 'text': ' Now.'}]
    