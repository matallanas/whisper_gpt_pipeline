import glob
import os
import validators
import pandas as pd
from downloader import WhisperPP, YoutubeDownloader
from interpreter import WhisperInterpreter
from datasets import load_dataset, concatenate_datasets, Dataset
from dataset.hf_dataset import HFDataset

class TranscriptDataset(HFDataset):

  def __init__(self, name) -> None:
    super().__init__(name)

  def generate_dataset(self, input, download_path, overwrite, whisper_config):
    if validators.url(input):
      self.from_url(input, download_path, overwrite, **whisper_config)
    else:
      self.from_files(input, overwrite,  **whisper_config)

  def from_url(self, url: str, download_path: str = "tmp/", overwrite: bool = False, **whisper_config: dict) -> None:
    if self.is_empty:
      emptyDataset = self.dataset
    else:
      #emptyDataset=self.dataset["train"].filter(lambda e: e["id"] is None)
      emptyDataset=self.dataset["train"]
    print(self.dataset.info)
    whisper_config["repoId"] = self.name
    whisperPP = WhisperPP(emptyDataset, **whisper_config)
    downloader = YoutubeDownloader(download_path)
    if not overwrite:
      downloader.config["download_archive"] = os.path.join(download_path,"video_record.txt")
      self._fill_archive(downloader.config["download_archive"])
    downloader.download(url, whisperPP)
    self._concatenate_datasets(whisperPP.get_data())

  def from_files(self, input:str, overwrite: bool = False, **whisper_config):
    if (whisper_config.get("mode", None) is not None):
      interpreter = WhisperInterpreter(whisper_config.pop("model_size"))
      process = getattr(interpreter, whisper_config.pop("mode"))
      result = process(input, **whisper_config)
      if type(result) == list:
        dataset = Dataset.from_list(result)
      else:
        dataset = Dataset.from_list([result])
    else:
      fileName = "tmp/*.json" if os.path.isdir(input) else input
      dataset=load_dataset("json", data_files=glob.glob(fileName), split="train")
    
    self._concatenate_datasets(dataset)

  def _fill_archive(self, archive_file):
    if not self.is_empty:
      with open(archive_file, "w") as f:
        for id in self.dataset["train"]["id"]:
          f.write(f"youtube {id}\n")

  def _concatenate_datasets(self, dataset):
    if not self.is_empty:
      selectedIDs = list(set(dataset["id"])-set(self.dataset["train"]["id"]))
      filteredDataset = dataset.filter(lambda element: element["id"] in selectedIDs)
      self.dataset["train"] = concatenate_datasets([self.dataset["train"],filteredDataset])
    else:
      self.dataset = dataset


