import threading
import logging
from pathlib import Path
from typing import List

from youtube_transcriber.datapipeline import DataPipeline

logging.basicConfig(level=logging.INFO, format="(%(threadName)-5s) %(message)s")

class ThreadedDataPipeline(threading.Thread):
    """Class that wraps a data pipeline in a thread."""

    def __init__(self,
                 data_pipeline: DataPipeline,
                 load_paths: List[Path],
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.data_pipeline = data_pipeline
        self.load_paths = load_paths
        
    def run(self) -> None:
        logging.info("Started processing data.")
        self.data_pipeline.process(self.load_paths)
        logging.info("Finished processing data.")