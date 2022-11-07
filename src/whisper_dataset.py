import click
import pandas as pd
from downloader import WhisperPP, YoutubeDownloader
from interpreter import WhisperInterpreter
from datasets import load_dataset

_global_options = [
  click.option("--model-size", default="base", help="Size of the model to use to transcribe"),
  click.option("--language", "-l", help="Language of the video"),
  click.option('--transcribe', 'mode', flag_value='transcribe', default=True),
  click.option('--translate', 'mode', flag_value='translate'),
  click.option("--write", "-w", is_flag=True, show_default=True, default=False, help="Write result in json.")
]

def global_options(func):
  for option in reversed(_global_options):
    func = option(func)
  return func

@click.group()
def cli():
  pass

@cli.command()
@click.argument("url")
@click.option("--download-path", "-d", default="tmp/", help="Path to download and store files")
@global_options
def download_url(url, download_path, model_size, language, mode, write):
  """
  Download a Youtube video and convert to mp3
  """
  data = []
  whisper_options = dict(
    model_size=model_size,
    mode=mode,
    language =language,
    write=write
  )
  whisperPP = WhisperPP(data, **whisper_options)
  downloader = YoutubeDownloader(download_path)
  downloader.download(url, whisperPP)
  return data

@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@global_options
def interpret(file_path, model_size, language, mode, write):
  """
  Transcribe or a tranlate a local file
  """
  interpreter = WhisperInterpreter(model_size)
  options = dict(language = language, write = write)
  process = getattr(interpreter, mode)
  result = process(file_path, **options)
  print(result)

@cli.command()
@click.argument("name")
@click.argument("url")
@click.option("--download-path", "-d", default="tmp/", help="Path to download and store files")
@global_options
@click.pass_context
def dataset(ctx, name, url, download_path, model_size, language, mode, write):
  """
  Add the transcript of Youtube videos to a Hugging Face dataset
  """

  #dataset = load_dataset(name)
  print(name)
  params = dict(
    url=url,
    download_path=download_path,
    model_size=model_size,
    language=language,
    mode=mode,
    write=write
  )
  result = ctx.invoke(download_url, **params)
  print(result)

if __name__ == "__main__":
  cli()