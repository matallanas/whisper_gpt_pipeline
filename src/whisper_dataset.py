import whisper
import click
import yt_dlp
import os
import json
import functools
import pandas as pd
from interpreter import WhisperInterpreter
from utils import VIDEO_INFO

def hook(d,data):
  if d['status'] == 'finished':
    select=["title","categories","tags"]
    data[d["info_dict"]["id"]] = {key: d["info_dict"][key] for key in select}

@click.group()
def cli():
  pass

# ℹ️ See help(yt_dlp.postprocessor.PostProcessor)
class MyCustomPP(yt_dlp.postprocessor.PostProcessor):
  def __init__(self,data,model_size):
    super().__init__()
    self.interpreter = WhisperInterpreter(model_size)
    self.data = data
  
  def run(self, info):
    self.to_screen('Doing stuff')
    #select=["id","channel","channel_id","title","categories","tags","description"]
    result = {key: info[key] for key in VIDEO_INFO}
    result["text"] = self.interpreter.transcribe(info["filepath"])["text"]
    self.data.append(result)
    #self.data[info['id']]["transcript"] = result["text"]
    #print(self.data)
    #with open("post_process.json","w") as outfile:
    #  json.dump(info,outfile)
    #print(info)
    return [], info


@cli.command()
#@click.option('--url', help='The url to download.')
@click.argument('url')
def download_url(url, download_path="tmp"):
  """
  Download a Youtube video and convert to mp3
  """
  
  data = []
  ydl_opts = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "audioformat": "mp3",
    "yesplaylist": True,
    "postprocessors": [{
      "key": "FFmpegExtractAudio",
      "preferredcodec": "mp3",
      "preferredquality": "192",
    }],
    "outtmpl": os.path.join(download_path,"%(id)s.%(ext)s"),
    #"progress_hooks": [functools.partial(hook, data=data)],
    #"download_archive": "video_record.txt"
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.add_post_processor(MyCustomPP(data,"base"), when='post_process')
    ydl.download(url)

  print(pd.DataFrame(data))
  return data
  

@cli.command()
@click.option('--file-path', help="Path to the audio file")
@click.option('--model-size', default="base", help="Size of the model to use to transcribe")
@click.option('--language', help="Language of the video")
@click.option('--transcribe', 'mode', flag_value='transcribe', default=True)
@click.option('--translate', 'mode', flag_value='translate')
def interpret(file_path, model_size, language, mode):
  interpreter = WhisperInterpreter(model_size)
  options = dict()
  if language is not None:
    options["language"] = language
    print(language)
  #options = dict(language=language)
  process = getattr(interpreter, mode)
  result = process(file_path, **options)
  print(result)

if __name__ == "__main__":
  cli()