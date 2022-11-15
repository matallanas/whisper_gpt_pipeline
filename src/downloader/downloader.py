from abc import ABC, abstractmethod


class Downloader(ABC):
  """Video downloader from online platforms to a specified format."""

  @abstractmethod
  def __init__(self, download_path: str):
    """Initialize the download_path.

    Args:
      download_path: str, Path where the resultant format is going to be stored.
    """
    self.download_path = download_path

  @abstractmethod
  def download(self):
    pass
