import os
import yt_dlp
from downloader import Downloader
from yt_dlp.postprocessor import PostProcessor
from utils import YT_OPTIONS

class YoutubeDownloader(Downloader):
  
  def __init__(self, download_path:str) -> None:
    super().__init__(download_path)
    self._ydl_options = YT_OPTIONS
    self._ydl_options["outtmpl"] = os.path.join(download_path,"%(id)s.%(ext)s")


  def download(self, url: str, CustomPP: PostProcessor, when: str = "post_process") -> None:
    with yt_dlp.YoutubeDL(self._ydl_options) as ydl:
      ydl.add_post_processor(CustomPP, when=when)
      ydl.download(url)
  
  @property
  def config(self):
    return self._ydl_options

  @config.setter
  def config(self, key: str, value: str) -> None:
    self._ydl_options[key] = value