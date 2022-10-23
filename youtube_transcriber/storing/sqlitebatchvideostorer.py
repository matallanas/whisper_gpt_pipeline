import json
import sqlite3
from typing import List, Tuple

from youtube_transcriber.utils import accepts_types
from youtube_transcriber.video import YoutubeVideo

class SQLiteBatchVideoStorer:
    """This is class is responsible to insert batch video entries in the db."""
    
    def __init__(self, table: str = "video"):
        self.table = table
    
    @accepts_types(sqlite3.Cursor, list) 
    def store(self,
              db_cursor: sqlite3.Cursor,
              videos: List[YoutubeVideo]) -> None:
        """Batch insert list of videos in the 'video' table of the db."""
        video_list = self._convert_videos_to_list(videos)
        db_cursor.executemany(f"INSERT INTO {self.table}(channel_name, url, title, description, transcription, segments) VALUES(?, ?, ?, ?, ?, ?)", 
                              video_list)
        
    @staticmethod 
    def _convert_videos_to_list(videos: List[YoutubeVideo]) -> List[Tuple[str, str, str, str, str, str]]:
        for video in videos:
            # TODO: Find better way to solve this
            video.segments = json.dumps(video.segments)
        return [video.to_tuple() for video in videos]