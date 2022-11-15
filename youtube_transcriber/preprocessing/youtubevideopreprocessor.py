from typing import List, Generator, Tuple
from pathlib import Path
from itertools import islice

import scrapetube
from youtubesearchpython import ChannelsSearch

from youtube_transcriber.utils import accepts_types
from youtube_transcriber.loading.serialization import Serializer

class YoutubeVideoPreprocessor:
    """This class is responsible for creating json files of expected as YoutubeVideo
    objects taking a channel name as input.
    Each JSON file has the following information:
    - channel_name: The name of the YouTube channel
    - url: The url of the video
    Args:
        channel_name (`str`):
            The name of the YouTube channel:
    Returns:
        load_paths (`List[Path]`)
            The paths of the json files of the video of that channel.
    TODO: Change it to accept also URL of video list, name of video list, etc.
    """
    def __init__(self, 
                 mode: str = "channel_name", 
                 serializer = Serializer) -> None:
        self.mode = mode
        self.serializer = serializer
    
    def preprocess(self,
                   name: str,
                   num_videos: int,
                   videos_in_ds: List[str]) -> Tuple[List[Path], Path]:
        if self.mode == "channel_name":
            # TODO: Add credits
            channels_search = ChannelsSearch(name, limit=1)
            channel_id = channels_search.result()['result'][0]['id']
            videos = scrapetube.get_channel(channel_id=channel_id)
            load_paths, dataset_folder = self._convert_videos_to_json_files(name, 
                                                                            videos, 
                                                                            num_videos,
                                                                            videos_in_ds)
            return load_paths, dataset_folder
        else:
            # TODO: implement this part
            youtube_folder = Path.home()/"whisper_gpt_pipeline/youtube_transcriber"
            test_files_folder = youtube_folder/"test/files"
            return [Path("test.json"), Path("test1.json")], test_files_folder

    def _convert_videos_to_json_files(self, 
                                      name:str, 
                                      videos: Generator,
                                      num_videos: int,
                                      videos_in_ds: List[str]) -> Tuple[List[Path], Path]:
        load_paths = []
        youtube_folder = Path.home()/"whisper_gpt_pipeline/youtube_transcriber"
        dataset_folder = youtube_folder/name
        Path(dataset_folder).mkdir(parents=True, exist_ok=True)
        i = 0
        while i < num_videos:
            try:
                video = next(videos)
                if video["videoId"] in videos_in_ds:
                    continue
                else:
                    file_name = f"{i}.json"
                    save_path = Path(dataset_folder, file_name)
                    save_path.touch(exist_ok=True)
                    video_dict = {"channel_name": name,
                                  "url":f"https://www.youtube.com/watch?v={video['videoId']}"}
                    self.serializer.dump(obj=video_dict, save_path=save_path)
                    load_paths.append(save_path)
                    i += 1
            except StopIteration:
                break
        return load_paths, dataset_folder