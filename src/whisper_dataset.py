import whisper
import click
import yt_dlp
import os

@click.command()
@click.option('--url', prompt='Youtube URL',
              help='The person to greet.')
def download_url(url, download_path="tmp"):
  """
  A way to trascribe a Youtube video
  """
  #URL = ['https://www.youtube.com/watch?v=uUkWJBmhOdw&ab_channel=StarTalk']

  ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'yesplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    "outtmpl": os.path.join(download_path,"%(id)s.%(ext)s"),
    "downloadarchive": "video_record.txt"
  }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(url)
  

def transcribe(file="example_audio.mp3"):
  model = whisper.load_model("medium")
  print("model Loaded")
  result = model.transcribe(file)
  print(result)

if __name__ == "__main__":
  download_url()
  #transcribe()