import os
import pytest
import sqlite3
from pathlib import Path

from youtube_transcriber.datapipeline import DataPipeline
from youtube_transcriber.datapipeline import create_hardcoded_data_pipeline
from youtube_transcriber.preprocessing.youtubevideopreprocessor import YoutubeVideoPreprocessor
from youtube_transcriber.loading.loaderiterator import LoaderIterator
from youtube_transcriber.loading.serialization import JsonSerializer
from youtube_transcriber.transforming.addtitletransform import AddTitleTransform
from youtube_transcriber.transforming.adddescriptiontransform import AddDescriptionTransform
from youtube_transcriber.transforming.whispertransform import WhisperTransform
from youtube_transcriber.transforming.batchtransformer import BatchTransformer
from youtube_transcriber.storing.sqlitebatchvideostorer import SQLiteBatchVideoStorer
from youtube_transcriber.storing.sqlitecontextmanager import SQLiteContextManager
from youtube_transcriber.storing.createdb import create_db

@pytest.fixture
def expected_db_output():
    return [
        ("Tquotes",
         "https://www.youtube.com/watch?v=NSkoGZ8J1Ag",
         "Steve Jobs quotes Bob Dylan", 
         " Good morning. Good morning and welcome to Apple's 1984 annual shareholders meeting. I'd like to open the meeting with a part of an old poem about a 20-year-old poem by Dylan. That's Bob Dylan. Come writers and critics who prophesize with your pens and keep your eyes wide, the chance won't come again. And don't speak too soon for the wheels still in spin. And there's no telling who that it's naming. For the loser now will be later to win for the times they are a change in. Now."),
        ("changminjen",
         "https://www.youtube.com/watch?v=Ak516vtDTEA",
         "My allegiance is to the Republic, to democracy!", 
         " I have brought peace, freedom, justice and security to my new empire. Your new empire don't make me kill you. Anakin, my allegiance is to the Republic, to democracy! If you're not with me, then you're my enemy. Only a Sith deals an absolute.")
    ]

@pytest.fixture
def data_pipeline():
    loader_iterator = LoaderIterator(JsonSerializer(), 2)
    batch_transformer = BatchTransformer([AddTitleTransform(),
                                          AddDescriptionTransform(),
                                          WhisperTransform()])
    video_storer = SQLiteBatchVideoStorer()
    sqlite_context_manager = SQLiteContextManager("dummy.db")
    return DataPipeline(loader_iterator,
                        batch_transformer,
                        video_storer,
                        sqlite_context_manager)

def test_datapipeline_init():
    data_pipeline = DataPipeline("loader_iterator",
                                 "transformer",
                                 "storer",
                                 "context")
    assert type(data_pipeline) == DataPipeline
    assert data_pipeline.loader_iterator == "loader_iterator"
    assert data_pipeline.batch_transformer == "transformer"
    assert data_pipeline.storer == "storer"
    assert data_pipeline.sqlite_context_manager == "context"
    
def test_process_files(data_pipeline, expected_db_output):
    test_folder = Path.home()/"whisper_gpt_pipeline/youtube_transcriber/test"
    files = [Path(test_folder/"files/6.json"), Path(test_folder/"files/7.json")]
    try:
        create_db("dummy.db")
        connection = sqlite3.connect("dummy.db")
        cursor = connection.cursor()
        
        data_pipeline.process(files)
        
        cursor.execute("SELECT CHANNEL_NAME, URL, TITLE, TRANSCRIPTION FROM VIDEO")
        videos = cursor.fetchall()
        
        for i in range(len(videos)):
            assert videos[i][0] == expected_db_output[i][0]
            assert videos[i][1] == expected_db_output[i][1]
            assert videos[i][2] == expected_db_output[i][2]
            assert videos[i][3] == expected_db_output[i][3]
    finally:
        os.remove("dummy.db")

def test_process_video_batch(data_pipeline, expected_db_output):
    video_data = [
        {
            "channel_name": "Tquotes",
            "url": "https://www.youtube.com/watch?v=NSkoGZ8J1Ag",
        },
        {
            "channel_name": "changminjen",
            "url": "https://www.youtube.com/watch?v=Ak516vtDTEA",
        }
    ]
    try:
        create_db("dummy.db")
        connection = sqlite3.connect("dummy.db")
        cursor = connection.cursor()

        data_pipeline._process_video_batch(cursor, video_data)

        cursor.execute("SELECT CHANNEL_NAME, URL, TITLE, TRANSCRIPTION FROM VIDEO")
        videos = cursor.fetchall()

        for i in range(len(videos)):
            assert videos[i][0] == expected_db_output[i][0]
            assert videos[i][1] == expected_db_output[i][1]
            assert videos[i][2] == expected_db_output[i][2]
            assert videos[i][3] == expected_db_output[i][3]
    finally:
        os.remove("dummy.db")
        
def test_hardcoded_data_pipeline_is_instantiated():
    data_pipeline = create_hardcoded_data_pipeline()
    assert type(data_pipeline) == DataPipeline      