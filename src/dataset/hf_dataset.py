from abc import ABC, abstractmethod
from datasets import load_dataset, Dataset
from datasets.data_files import EmptyDatasetError

class HFDataset(ABC):
  """
  Create a dataset to save the transcripts from Youtube.
  """
  def __init__(self, name) -> None:
    self.name = name
    if name != "":
      self._init_dataset()
    else:
      self.dataset = Dataset.from_dict({})
      self.exist = False
      self.is_empty = True

  @abstractmethod
  def generate_dataset():
    pass

  def _init_dataset(self):
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
    self.dataset.push_to_hub(self.name)