from typing import Dict, List
from pathlib import Path
from sqlite3 import Cursor

from youtube_transcriber.utils import accepts_types, create_videos
from youtube_transcriber.preprocessing.youtubevideopreprocessor import YoutubeVideoPreprocessor
from youtube_transcriber.loading.loaderiterator import LoaderIterator
from youtube_transcriber.transforming.batchtransformer import BatchTransformer
from youtube_transcriber.storing.sqlitebatchvideostorer import SQLiteBatchVideoStorer
from youtube_transcriber.storing.sqlitecontextmanager import SQLiteContextManager
from youtube_transcriber.loading.serialization import JsonSerializer
from youtube_transcriber.transforming.addtitletransform import AddTitleTransform
from youtube_transcriber.transforming.adddescriptiontransform import AddDescriptionTransform
from youtube_transcriber.transforming.whispertransform import WhisperTransform

class DataPipeline:
    """A class that wraps the different components of the system. It processes
    data using these steps: preprocess -> load -> apply transform -> store.
    """
    
    def __init__(self,
                 video_preprocessor: YoutubeVideoPreprocessor,
                 loader_iterator: LoaderIterator,
                 batch_transformer: BatchTransformer,
                 storer: SQLiteBatchVideoStorer,
                 sqlite_context_manager: SQLiteContextManager) -> None:
        self.video_preprocessor = video_preprocessor
        self.loader_iterator = loader_iterator
        self.batch_transformer = batch_transformer
        self.storer = storer
        self.sqlite_context_manager = sqlite_context_manager
        
    @accepts_types(list)
    def process(self, channel_name: str, num_videos: int) -> None:
        """Process files in batches: preprocess -> load -> transform -> store to db."""
        load_paths = self.video_preprocessor.preprocess(channel_name, num_videos)
        self.loader_iterator.load_paths = load_paths
        with self.sqlite_context_manager as db_cursor:
            for video_data_batch in self.loader_iterator:
                self._process_video_batch(db_cursor, video_data_batch)
    
    def _process_video_batch(self,
                             db_cursor: Cursor,
                             video_data_batch: List[Dict]) -> None:
        videos = create_videos(video_data_batch)
        transformed_videos = self.batch_transformer.apply(videos)
        self.storer.store(transformed_videos)

def create_hardcoded_data_pipeline() -> DataPipeline:
    """Factory function to create a DataPipeline with 
    default arguments. 
    TODO: Create DataPipeline so users can pass the args.
    """
    yt_video_preprocessor = YoutubeVideoPreprocessor()
    loader_iterator = LoaderIterator(JsonSerializer(), 2)
    # Whisper transform using based model and timestamps
    # TODO: Let user select this parameters.
    batch_transformer = BatchTransformer([AddTitleTransform(),
                                          AddDescriptionTransform(),
                                          WhisperTransform()])
    video_storer = SQLiteBatchVideoStorer()
    sqlite_context_manager = SQLiteContextManager("video.db")
    return DataPipeline(yt_video_preprocessor,
                        loader_iterator,
                        batch_transformer,
                        video_storer,
                        sqlite_context_manager)   