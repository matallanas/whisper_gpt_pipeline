import glob
import os
from typing import Any, Optional
import validators
from downloader import WhisperPP, YoutubeDownloader
from interpreter import WhisperInterpreter
from datasets import load_dataset, concatenate_datasets, Dataset
from dataset.hf_dataset import HFDataset


class TranscriptDataset(HFDataset):
  """Create a TranscriptDataset."""

  def __init__(self, name: str, token: Optional[str] = None):
    """A decorator to initialize the class.

    Args:
        name (str): Repository id
    """
    super().__init__(name, token)

  def generate_dataset(
      self,
      input: str,
      download_path: str,
      overwrite: bool,
      whisper_postprocessor_config: Optional[Any]
    ):
    """Generate a transcript dataset from audio transcriptions.

    Args:
        input (str): An url, a path or afile to make the transcription.
        download_path (str): Path to store all the files downloaded.
        overwrite (bool): Flag to overwrite the data transcription.
        **whisper_postprocessor_config (Optional[Any]): Dictionary with the 
        configuration of the postprocessor.
    """
    if validators.url(input):
      self.from_url(input, download_path, overwrite, **whisper_postprocessor_config)
    else:
      self.from_files(input, overwrite,  **whisper_postprocessor_config)

  def from_url(
      self,
      url: str,
      download_path: str = "tmp/",
      overwrite: bool = False,
      **whisper_postprocessor_config: dict
    ):
    """Loads the whisper dataset from a URL.

    Args:
        url (str): Url to download the video.
        download_path (str, optional): Path to store all the files downloaded.
        Defaults to "tmp/".
        overwrite (bool, optional): Flag to overwrite the data transcription.
        Defaults to False.
        **whisper_postprocessor_config (Optional[Any]): Dictionary with the 
        configuration of the postprocessor.
    """
    if self.is_empty:
      emptyDataset = self.dataset
    else:
      emptyDataset=self.dataset["train"]
    whisper_postprocessor_config["repoId"] = self.name
    whisper_postprocessor_config["token"] = self.token
    whisperPP = WhisperPP(emptyDataset, **whisper_postprocessor_config)
    downloader = YoutubeDownloader(download_path)
    if not overwrite:
      downloader.config["download_archive"] = os.path.join(download_path,"video_record.txt")
      self._fill_archive(downloader.config["download_archive"])
    downloader.download(url, whisperPP)
    self._concatenate_datasets(whisperPP.get_data())

  def from_files(
      self,
      input:str,
      overwrite: bool = False,
      **whisper_postprocessor_config
    ):
    """Loads dataset from files.

    Args:
        input (str): Input path or file to create the dataset.
        overwrite (bool, optional): Flag to overwrite the data transcription.
        Defaults to False.
        **whisper_postprocessor_config (Optional[Any]): Dictionary with the 
        configuration of the postprocessor.
    """
    if (whisper_postprocessor_config.get("mode", None) is not None):
      interpreter = WhisperInterpreter(whisper_postprocessor_config.pop("model_size"))
      process = getattr(interpreter, whisper_postprocessor_config.pop("mode"))
      whisper_postprocessor_config["write"] = overwrite
      result = process(input, **whisper_postprocessor_config)
      if type(result) == list:
        dataset = Dataset.from_list(result)
      else:
        dataset = Dataset.from_list([result])
    else:
      fileName = "tmp/*.json" if os.path.isdir(input) else input
      dataset=load_dataset("json", data_files=glob.glob(fileName), split="train")
    
    self._concatenate_datasets(dataset)

  def _fill_archive(self, archive_file: str):
    """Write the youtube dataset if not empty .

    Args:
        archive_file (str): File path to the archive file from previous stored 
        transcripted videos.
    """
    if not self.is_empty:
      with open(archive_file, "w") as f:
        for id in self.dataset["train"]["id"]:
          f.write(f"youtube {id}\n")

  def _concatenate_datasets(self, dataset):
    """Concatenate dataset with previos ids and not having duplicates.

    Args:
        dataset (list | Dataset): Data of video transcription.
    """
    if not self.is_empty:
      selectedIDs = list(set(dataset["id"])-set(self.dataset["train"]["id"]))
      filteredDataset = dataset.filter(lambda element: element["id"] in selectedIDs)
      self.dataset["train"] = concatenate_datasets([self.dataset["train"],filteredDataset])
    else:
      self.dataset = dataset
