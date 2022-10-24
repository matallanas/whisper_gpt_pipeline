import os
import pytest
import sqlite3

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
        ("MrBeast Shorts",
         "https://www.youtube.com/watch?v=mJ4t7iNF86g",
         "I Am The World's Strongest Hero", 
         " What am I favorite anime has been adapted into a game? One bunch man the strongest is a strategic term based RPG game where you need to recruit heroes and villains to create the strongest lineup in the world. Is that what they love? Chiometimes faites adventure when worker Coca Inspirates принципs coming from spawn in the ship. The answer list is a promo post芝 not deeeeee chocolate but cheese"),
        ("MrBeast Shorts",
         "https://www.youtube.com/watch?v=UPhxU9J46Qk",
         "Where Chocolate REALLY Comes From", 
         " This is a cacao pod. How do you open it? I like to karate chop. I was a clean great. This is where chocolate comes from. Oh my goodness. This right here is 99% of what's in here. So all you do is ferment these seeds right here. Blend it all up with some sugar and then you've got your chocolate. Taste test. Rocket Calvars is our refined chocolate bars. I don't even need to taste it. This one.")
    ]

@pytest.fixture
def data_pipeline():
    video_preprocessor = YoutubeVideoPreprocessor(mode="channel_name", 
                                                  serializer=JsonSerializer())
    loader_iterator = LoaderIterator(JsonSerializer(), 2)
    batch_transformer = BatchTransformer([AddTitleTransform(),
                                          AddDescriptionTransform(),
                                          WhisperTransform()])
    video_storer = SQLiteBatchVideoStorer()
    sqlite_context_manager = SQLiteContextManager("dummy.db")
    return DataPipeline(video_preprocessor,
                        loader_iterator,
                        batch_transformer,
                        video_storer,
                        sqlite_context_manager)

def test_datapipeline_init():
    data_pipeline = DataPipeline("video_preprocessor",
                                 "loader_iterator",
                                 "transformer",
                                 "storer",
                                 "context")
    assert type(data_pipeline) == DataPipeline
    assert data_pipeline.video_preprocessor == "video_preprocessor"
    assert data_pipeline.loader_iterator == "loader_iterator"
    assert data_pipeline.batch_transformer == "transformer"
    assert data_pipeline.storer == "storer"
    assert data_pipeline.sqlite_context_manager == "context"
    
def test_process_files(data_pipeline, expected_db_output):
    try:
        create_db("dummy.db")
        connection = sqlite3.connect("dummy.db")
        cursor = connection.cursor()
        
        data_pipeline.process("MrBeast Shorts", num_videos=2)
        
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
            "channel_name": "MrBeast Shorts",
            "url": "https://www.youtube.com/watch?v=mJ4t7iNF86g",
        },
        {
            "channel_name": "MrBeast Shorts",
            "url": "https://www.youtube.com/watch?v=UPhxU9J46Qk",
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