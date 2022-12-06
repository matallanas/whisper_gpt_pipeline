from typing import Any
import click
from dataset import TranscriptDataset
from downloader import WhisperPP, YoutubeDownloader
from interpreter import WhisperInterpreter
from utils import AUDIO_FORMAT


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
@click.option("--audio", "-a", is_flag=True, show_default=True, default=False,
    help="Add audio feature to the dataset with the audio extracted.")
@click.option("--audio-format", "-f", default="mp3",
    type=click.Choice(AUDIO_FORMAT, case_sensitive=False),
    help="Specific audio format")
@click.option("--upload", "-u", is_flag=True, show_default=True, default=False,
    help="Upload dataset to the hub.")
@click.option("--number-videos", "-v", default=0, help="Number of videos to process.")
@click.option("--overwrite", "-o", is_flag=True, default=False, help="Overwrite the data.")
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
  audio: bool,
  audio_format: str,
  number_videos: int,
  overwrite: bool
):
  """
  Add the transcript of Youtube videos to a Hugging Face dataset
  """

  ds = TranscriptDataset(name, token, audio)
  params = dict(
    model_size=model_size,
    language=language,
    write=write,
    audio_format = audio_format.lower(),
    number_videos=number_videos)
  if mode is not None:
    params["mode"] = mode
  ds.generate_dataset(input, download_path, overwrite, params)
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
@click.option("--audio", "-a", is_flag=True, show_default=True, default=False,
    help="Add audio feature to the dataset with the audio extracted.")
@click.option("--audio-format", "-f", default="mp3",
    type=click.Choice(AUDIO_FORMAT, case_sensitive=False),
    help="Specific audio format")
@click.option("--upload", "-u", is_flag=True, show_default=True, default=False,
    help="Upload dataset to the hub.")
@click.option("--number-videos", "-v", default=0, help="Number of videos to process.")
@click.option("--overwrite", "-o", is_flag=True, default=False, help="Overwrite the data.")
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
  audio: bool,
  audio_format: str,
  number_videos: int,
  overwrite: bool
):
  """
  Add the transcript of Youtube videos to a Hugging Face dataset
  """

  ds = TranscriptDataset(name, token, audio)
  i = 339
  print(ds.dataset["train"].select([['id', 'channel', 'channel_id', 'title', 'categories', 'tags', 'description', 'text', 'segments']]))
  # for e in ds.dataset["train"]:
  #   title = e["title"]
  #   if '#' in title:
  #     print(f'{i} - {title.split("#")[1]}')
  #   else:
  #     print(f'{i} - {title}')
  #   i -= 1 


if __name__ == "__main__":
  cli()
