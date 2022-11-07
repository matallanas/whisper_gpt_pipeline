from abc import ABC, abstractmethod
 
class Downloader(ABC):
  """
  A video downloader from online platforms to a specified format
  """

  @abstractmethod
  def __init__(self, download_path):
    self.download_path = download_path

  @abstractmethod
  def download(self):
    pass