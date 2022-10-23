from typing import List, Generator
from pathlib import Path
from itertools import islice

from youtubesearchpython import ChannelsSearch
import scrapetube

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
                   num_videos: int) -> List[Path]:
        if self.mode == "channel_name":
            # TODO: Add credits
            channelsSearch = ChannelsSearch(name, limit=1)
            videos = scrapetube.get_channel(channelsSearch.result()['result'][0]['id'])
            load_paths = self._convert_videos_to_json_files(name, videos, num_videos)
            return load_paths
        else:
            # TODO: implement this part
            return [Path("test.json"), Path("test1.json")]

    def _convert_videos_to_json_files(self, 
                                      name:str, 
                                      videos: Generator,
                                      num_videos: int) -> List[Path]:
        load_paths = []
        youtube_folder = Path.home()/"whisper_gpt_pipeline/youtube_transcriber"
        dataset_folder = youtube_folder/name
        Path(dataset_folder).mkdir(parents=True, exist_ok=True)
        for index, video in enumerate(islice(videos, num_videos)):
            file_name = f"{index}.json"
            save_path = Path(dataset_folder, file_name)
            save_path.touch(exist_ok=True)
            video_dict = {"channel_name": name, 
                          "url":f"https://www.youtube.com/watch?v={video['videoId']}"}
            self.serializer.dump(video_dict, save_path)
            load_paths.append(save_path)
        return load_paths