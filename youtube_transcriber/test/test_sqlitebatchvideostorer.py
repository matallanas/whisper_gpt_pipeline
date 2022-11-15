import os
from collections import OrderedDict
import sqlite3
import pytest

from youtube_transcriber.storing.createdb import create_db
from youtube_transcriber.storing.sqlitebatchvideostorer import SQLiteBatchVideoStorer
from youtube_transcriber.video import YoutubeVideo

@pytest.fixture
def videos():
    return [YoutubeVideo(channel_name="Tquotes", url="https://www.youtube.com/watch?v=NSkoGZ8J1Ag", 
                         title="Steve Jobs quotes Bob Dylan", description="", 
                         transcription=" Good morning. Good morning and welcome to Apple's 1984 annual shareholders meeting. I'd like to open the meeting with a part of an old poem about a 20-year-old poem by Dylan. That's Bob Dylan. Come writers and critics who prophesize with your pens and keep your eyes wide, the chance won't come again. And don't speak too soon for the wheels still in spin. And there's no telling who that it's naming. For the loser now will be later to win for the times they are a change in. Now.",
                         segments=[OrderedDict({'start': 0.0, 'end': 2.0, 'text': ' Good morning.'})]),
            YoutubeVideo(channel_name="changminjen", url="https://www.youtube.com/watch?v=Ak516vtDTEA",
                         title="My allegiance is to the Republic, to democracy!", description="Anakin, my allegiance is to the Republic, to democracy! from Star Wars Episode III: Revenge of the Sith.",
                         transcription=" I have brought peace, freedom, justice and security to my new empire. Your new empire dont make me kill you. Anakin, my allegiance is to the Republic, to democracy! If you're not with me, then you're my enemy. Only a Sith deals an absolute.",
                         segments=[OrderedDict({'start': 0.0, 'end': 8.0, 'text': ' I have brought peace, freedom, justice and security to my new empire.'}),
                                   OrderedDict({'start': 8.0, 'end': 14.0, 'text': " Your new empire dont make me kill you."})])]

@pytest.fixture
def expected_video_list():
    return [("Tquotes", "https://www.youtube.com/watch?v=NSkoGZ8J1Ag", "Steve Jobs quotes Bob Dylan", "", 
             " Good morning. Good morning and welcome to Apple's 1984 annual shareholders meeting. I'd like to open the meeting with a part of an old poem about a 20-year-old poem by Dylan. That's Bob Dylan. Come writers and critics who prophesize with your pens and keep your eyes wide, the chance won't come again. And don't speak too soon for the wheels still in spin. And there's no telling who that it's naming. For the loser now will be later to win for the times they are a change in. Now.", 
             '[{"start": 0.0, "end": 2.0, "text": " Good morning."}]'),
            ("changminjen", "https://www.youtube.com/watch?v=Ak516vtDTEA", "My allegiance is to the Republic, to democracy!", "Anakin, my allegiance is to the Republic, to democracy! from Star Wars Episode III: Revenge of the Sith.",
             " I have brought peace, freedom, justice and security to my new empire. Your new empire dont make me kill you. Anakin, my allegiance is to the Republic, to democracy! If you're not with me, then you're my enemy. Only a Sith deals an absolute.",
             '[{"start": 0.0, "end": 8.0, "text": " I have brought peace, freedom, justice and security to my new empire."}, {"start": 8.0, "end": 14.0, "text": " Your new empire dont make me kill you."}]')]

def test_sqlite_batch_video_storer_init():
    video_storer = SQLiteBatchVideoStorer("table")
    assert type(video_storer) == SQLiteBatchVideoStorer
    assert video_storer.table == "table"
    
def test_convert_videos_to_list(videos, expected_video_list):
    videos_list = SQLiteBatchVideoStorer._convert_videos_to_list(videos)
    assert videos_list == expected_video_list
    
def test_videos_are_insterted_in_db(videos, expected_video_list):
    try:
        create_db("dummy.db")
        video_storer = SQLiteBatchVideoStorer("video")
        connection = sqlite3.connect("dummy.db")
        cursor = connection.cursor()
        
        video_storer.store(cursor, videos)
        cursor.execute("SELECT CHANNEL_NAME, URL, TITLE, DESCRIPTION, TRANSCRIPTION, SEGMENTS FROM VIDEO")
        videos = cursor.fetchall()
        
        assert videos == expected_video_list
    finally:
        os.remove("dummy.db")