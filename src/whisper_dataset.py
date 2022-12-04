import glob
import json
import os
from typing import Any
import click
from dataset import TranscriptDataset
from datasets import load_dataset, Dataset, Audio
from downloader import WhisperPP, YoutubeDownloader
from interpreter import WhisperInterpreter
from utils import AUDIO_FEATURE, json_dump


_global_options = [
  click.option("--model-size", "-m", default="base",
    help="Size of the model to use to transcribe"),
  click.option("--language", "-l", help="Language of the video"),
  click.option("--transcribe", "mode", flag_value="transcribe",
    help="Transcribe audio files to its language."),
  click.option("--translate", "mode", flag_value="translate",
    help="Traslate audio files to its language."),
  click.option("--write", "-w", is_flag=True, show_default=True, default=False,
    help="Write result in a json."),
]


def global_options(func: Any):
  for option in reversed(_global_options):
    func = option(func)
  return func


@click.group()
def cli():
  pass


@cli.command()
@click.argument("url")
@click.option("--download-path", "-d", default="tmp/",
              help="Path to download and store files")
@global_options
def download_url(
  url: str,
  download_path: str,
  model_size: str,
  language: str,
  mode: str,
  write: bool
):
  """
  Download a Youtube video and convert to mp3
  """
  data = []
  whisper_options = dict(
    model_size=model_size,
    mode="transcribe" if mode is None else mode, 
    language=language,
    write=write
  )
  whisperPP = WhisperPP(data, **whisper_options)
  downloader = YoutubeDownloader(download_path)
  downloader.download(url, whisperPP)
  return data


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@global_options
def interpret(file_path: str, model_size: str, language: str, mode: str, write: bool):
  """
  Transcribe or a tranlate a local file
  """
  interpreter = WhisperInterpreter(model_size)
  options = dict(
    language=language,
    write=write
  )
  process = getattr(interpreter, "transcribe" if mode is None else mode)
  result = process(file_path, **options)
  print(result)


@cli.command()
@click.option("--name", "-n", default="",
    help="Name of the Hugging Face Dataset, if empyt a local dataset is created.")
@click.option("--token", "-t", default=None,
    help="token of the repository to read and/or write.")
@click.option("--input", "-i",
    help="Location of the data, could be youtube url or a local path.")
@click.option("--download-path", "-d", default="tmp/",
    help="Path to download and store files.")
@click.option("--upload", "-u", is_flag=True, show_default=True, default=False,
    help="Upload dataset to the hub.")
@click.option("--number-videos", "-v", default=0, help="Number of videos to process.")
@click.option("--overwrite", "-o", default=False, help="Overwrite the data.")
@global_options
def dataset(
  name: str,
  token: str,
  input: str,
  download_path: str,
  upload: str,
  model_size: str,
  language: str,
  mode: str,
  write: bool,
  number_videos: int,
  overwrite: bool
):
  """
  Add the transcript of Youtube videos to a Hugging Face dataset
  """

  ds = TranscriptDataset(name, token)
  overwrite = False
  params = dict(
    model_size=model_size,
    language=language, 
    write=write,
    number_videos=number_videos)
  if mode is not None:
    params["mode"] = mode
  ds.generate_dataset(input, download_path, overwrite, params)
  print(ds.dataset)
  if upload or (overwrite and name != ""):
    ds.upload()

@cli.command()
@click.option("--name", "-n", default="",
    help="Name of the Hugging Face Dataset, if empyt a local dataset is created.")
@click.option("--token", "-t", default=None,
    help="token of the repository to read and/or write.")
@click.option("--input", "-i",
    help="Location of the data, could be youtube url or a local path.")
@click.option("--download-path", "-d", default="tmp/",
    help="Path to download and store files.")
@click.option("--upload", "-u", is_flag=True, show_default=True, default=False,
    help="Upload dataset to the hub.")
@click.option("--number-videos", "-v", default=0, help="Number of videos to process.")
@click.option("--overwrite", "-o", default=False, help="Overwrite the data.")
@global_options
def audio_dataset(
  name: str,
  token: str,
  input: str,
  download_path: str,
  upload: str,
  model_size: str,
  language: str,
  mode: str,
  write: bool,
  number_videos: int,
  overwrite: bool
):
  """
  Add the transcript of Youtube videos to a Hugging Face dataset
  """

  #ds = TranscriptDataset(name, token)
  # overwrite = False
  # params = dict(
  #   model_size=model_size,
  #   language=language, 
  #   write=write,
  #   number_videos=number_videos)
  # if mode is not None:
  #   params["mode"] = mode
  # ds.generate_dataset(input, download_path, overwrite, params)

  #print(ds.dataset)  
  groups = []
  group = []
  for file in glob.glob(os.path.join(input,"*.json")):
    group.append(file)
    if len(group)==1000:
      groups.append(group)
      group=[]
  
  groups.append(group)

  for group in groups:
    print(len(group))


  #ds.dataset.push_to_hub(repo_id=name, token=token)

  # Write the audio
  #print(glob.glob(os.path.join(input,"*.json")))
  #for file in glob.glob(os.path.join(input,"*.json")):
  #  with open(file,"r") as f:
  #    record = json.loads(f.read())
  #  record["audio"]=file.split('.')[0]+".mp3"
  #  json_dump(record, file)

  

  #result["audio"]="data/ZEhOhU8zRbk.mp3"
  #audio_dataset = Dataset.from_list(result)
  #audio_dataset = audio_dataset.cast_column(AUDIO_FEATURE, Audio())
  #print(audio_dataset[0]["audio"])
  #if upload or (overwrite and name != ""):
  #  ds.upload()


if __name__ == "__main__":
  cli()
