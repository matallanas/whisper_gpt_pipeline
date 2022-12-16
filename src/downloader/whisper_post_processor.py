import os
import re
from typing import Any, Optional, Union
from interpreter import WhisperInterpreter
from utils import AUDIO_FEATURE, VIDEO_INFO, json_dump
from yt_dlp.postprocessor import PostProcessor
from datasets import Dataset, Audio


class WhisperPP(PostProcessor):
  """Create a whisper postprocessor after downloading and extracting the audio 
  from a video.
  """

  def __init__(self, data: Union[list,Dataset], **whisper_options: Optional[Any]):
    """Initialize the dataset to process information.

    Args:
      data: list or Dataset, Data structure to fill with the result of the transcription.
      **whisper_options: Optional[Any], Options to process the audio with whisper.
    """
    super().__init__()
    self._options = whisper_options
    interpreter = WhisperInterpreter(self._options.pop("model_size","base"))
    self.data = data
    self._process = getattr(interpreter, self._options.pop("mode","transcribe"))
    self._write = self._options.pop("write")
    self.videos_to_process = self._options.pop("number_videos",0)
    self.repoId = self._options.pop("repoId",self._get_name())
    self.token = self._options.pop("token",None)
    self.audio = self._options.pop("audio",False)
  
  def run(self, info: Any):
    """Runs the process the audio extracted from the video through whisper.

    Args:
      info: Any, All the info extracted and tags from the video doenloaded.

    Returns:
      (list, Any): An empty list and an object needed by the yt_dlp library.
    """
    self.to_screen(f"Processing Video {info['id']}")
    result = {key: info[key] for key in VIDEO_INFO}
    result.update(self._process(info["filepath"], **self._options))
    self.to_screen(f"Processed Video {info['id']} and appended results.")
    self._update_data(result)
    if self._write:
      json_dump(result, f"{info['filepath'].split('.')[0]}.json")
    elif not self.audio:
      os.remove(info['filepath'])
    return [], info

  def _update_data(self, record: dict):
    """Update the data of the transcribed record added to a hugging face dataset 
    or to a list.

    Args:
      record: dict, Transcription of the video.
    """
    dataType = type(self.data)
    if dataType == list:
      self.data.append(record)
    else:
      self.data = self.data.add_item(record)
      if self.data.num_rows == 1 and self.audio:
        self.data = self.data.cast_column(AUDIO_FEATURE, Audio())
      if self.videos_to_process != 0 and self.data.num_rows%self.videos_to_process==0:
        self.data.push_to_hub(repo_id=self.repoId, token=self.token)

  def get_data(self):
    """Get the current data.

    Returns:
      list or Dataset: Get the dataset update after processing the video, list or 
      playlist.
    """
    return self.data
  
  def _get_name(self):
    """Get name of the dataset.

    Returns:
        str: Id of the repository.
    """
    if type(self.data) is Dataset and self.data.info.download_checksums is not None:
      regex = r"(?<=datasets\/)(.*?)(?=\/resolve)"
      repoId = re.compile(regex)
      url = list(self.data.info.download_checksums.keys())[0]
      return repoId.findall(url)[0]
    return ""
