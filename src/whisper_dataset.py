import whisper
import click
import yt_dlp
import os
import json
import functools

def hook(d,data):
    if d['status'] == 'finished':
        select=["title","categories","tags"]
        data[d["info_dict"]["id"]] = {key: d["info_dict"][key] for key in select}

@click.command()
@click.option('--url', help='The person to greet.')
def download_url(url, download_path="tmp"):
  """
  A way to trascribe a Youtube video
  """
  
  data = {}
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
    "progress_hooks": [functools.partial(hook, data=data)],
    "download_archive": "video_record.txt"
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(url)

  return data
  

def transcribe(file="example_audio.mp3"):
  model = whisper.load_model("medium")
  print("model Loaded")
  result = model.transcribe(file)
  print(result)

if __name__ == "__main__":
  download_url()
  #transcribe()