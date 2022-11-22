from abc import ABC, abstractmethod
from typing import Optional
from datasets import load_dataset, Dataset
from datasets.data_files import EmptyDatasetError


class HFDataset(ABC):
  """Create a dataset to save the transcripts from Youtube."""

  def __init__(self, name: str, token: Optional[str] = None):
    """Initialize the Hugging Face dataset.

    Args:
        name (str): repository ID of the dataset or name to dataset.
        token (Optional[str], optional): token to upload the dataset if necessary. 
        Defaults to None.
    """
    self.name = name
    self.token = token
    if name != "":
      self._init_dataset()
    else:
      self.dataset = Dataset.from_dict({})
      self.exist = False
      self.is_empty = True

  @abstractmethod
  def generate_dataset():
    """This method is called when you want to generate a dataset."""
    pass

  def _init_dataset(self):
    """Load dataset if exists."""
    try:
      self.dataset = load_dataset(self.name)
      self.exist = True
      self.is_empty = False
    except EmptyDatasetError:
      self.dataset = Dataset.from_dict({})
      self.exist = True
      self.is_empty = True
      pass
    except FileNotFoundError:
      self.dataset = Dataset.from_dict({})
      self.exist = False
      self.is_empty = True
      pass
  
  def upload(self):
    """Push the dataset to the hub."""
    self.dataset.push_to_hub(repo_id=self.name, token=self.token)
