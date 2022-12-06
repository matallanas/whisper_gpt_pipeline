import os
import yt_dlp
from downloader import Downloader
from yt_dlp.postprocessor import PostProcessor
from utils import YT_OPTIONS


class YoutubeDownloader(Downloader):
  """Download videos from youtube giving a configuration."""

  def __init__(self, download_path:str, audio_format:str = "mp3"):
    """Create a downloader from youtube using specifying the path to save the output.

    Args:
    download_path: str, Path to download the resulting files.
    """
    super().__init__(download_path)
    self._ydl_options = YT_OPTIONS
    self._ydl_options["outtmpl"] = os.path.join(download_path,"%(id)s.%(ext)s")
    if audio_format != "mp3":
      self._ydl_options["audioformat"] = audio_format
      self._ydl_options["postprocessors"][0]["preferredcodec"] = audio_format

  def download(self, url: str, CustomPP: PostProcessor, when: str = "post_process"):
    """Download the YouTube content.

    Args:
      url: str, Video, playlist or channel video list from youtube. 
      CustomPP: PostProcessor, A custom post processor to execute previous or after 
      the download.
      when: str, optional, When to execute the postprocessor. Defaults to 
      "post_process".
    """
    with yt_dlp.YoutubeDL(self._ydl_options) as ydl:
      ydl.add_post_processor(CustomPP, when=when)
      ydl.download(url)
  
  def download(self, url: str):
    """Download the YouTube content.

    Args:
      url: str, Video, playlist or channel video list from youtube.
    """
    with yt_dlp.YoutubeDL(self._ydl_options) as ydl:
      ydl.download(url)
  
  @property
  def config(self):
    """Returns the configuration with the default values.

    Returns:
      dict: Configuration dictionary
    """
    return self._ydl_options

  @config.setter
  def config(self, key: str, value: str):
    """Set configuration parameters for a YL document .

    Args
      key: str, Name of the property to modify
      value: str, Value of the property
    """
    self._ydl_options[key] = value
