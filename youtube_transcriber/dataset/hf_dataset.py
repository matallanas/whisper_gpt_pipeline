# Adapted from Eduardo Matallanas
from datasets import load_dataset, Dataset
from datasets.data_files import EmptyDatasetError

class HFDataset():
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

  def _init_dataset(self):
    try:
      self.dataset = load_dataset(self.name)
      self.exist = True
      self.is_empty = False
      self.list_of_ids = self._get_list_of_id()
    except EmptyDatasetError:
      self.dataset = Dataset.from_dict({})
      self.exist = True
      self.is_empty = True
      self.list_of_ids = []
      pass
    except FileNotFoundError:
      self.dataset = Dataset.from_dict({})
      self.exist = False
      self.is_empty = True
      self.list_of_ids = []
      pass

  def upload(self):
    self.dataset.push_to_hub(self.name)
    
  def _get_list_of_id(self):
    new_ds = self.dataset.map(
      lambda x: {"ID": [url.split("=")[-1] for url in x["URL"]]}, batched=True
    )
    list_of_ids = []
    for split in new_ds:
      ids = new_ds[split]["ID"]
      list_of_ids.append(ids)
    return [item for sublist in list_of_ids for item in sublist]