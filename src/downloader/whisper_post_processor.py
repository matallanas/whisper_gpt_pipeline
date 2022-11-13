from interpreter import WhisperInterpreter
from utils import VIDEO_INFO, json_dump
from yt_dlp.postprocessor import PostProcessor
from datasets import Dataset
import re

class WhisperPP(PostProcessor):
  def __init__(self,data,**whisper_options):
    super().__init__()
    self._options = whisper_options
    interpreter = WhisperInterpreter(self._options.pop("model_size","base"))
    self.data = data
    self._process = getattr(interpreter, self._options.pop("mode","transcribe"))
    self._write = self._options.pop("write")
    self.videos_to_process = self._options.pop("number_videos",0)
    print(self.videos_to_process)
    self.repoId = self._options.pop("repoId",self._get_name():quit)
    print(self.repoId)
  
  def run(self, info):
    self.to_screen(f"Processing Video {info['id']}")
    result = {key: info[key] for key in VIDEO_INFO}
    result.update(self._process(info["filepath"], **self._options))
    self.to_screen(f"Processed Video {info['id']} and appended results.")
    self._update_data(result)
    if self._write:
      json_dump(result, f"{info['filepath'].split('.')[0]}.json")
    return [], info

  def _update_data(self, record):
    dataType = type(self.data)
    if dataType == list:
      self.data.append(record)
    else:
      self.data = self.data.add_item(record)
      if self.data.num_rows%self.videos_to_process==0 and self.videos_to_process != 0:
        self.data.push_to_hub(self.repoId)

  def get_data(self):
    return self.data

  def _get_name(self):
    if self.data.info.download_checksums is not None:
      regex = r"(?<=datasets\/)(.*?)(?=\/resolve)"
      repoId = re.compile(regex)
      url = list(self.data.info.download_checksums.keys())[0]
      return repoId.findall(url)[0]
    return ""
    