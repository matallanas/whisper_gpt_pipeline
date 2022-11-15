import pytest

from youtube_transcriber.dataset.hf_dataset import HFDataset

@pytest.fixture
def hf_test_dataset():
    hf_dataset = HFDataset("Whispering-GPT/test_whisper")
    return hf_dataset

def test_hf_dataset_init(hf_test_dataset):
    assert hf_test_dataset.exist == True
    assert hf_test_dataset.is_empty == False
    
def test_get_list_of_ids(hf_test_dataset):
    expected_list = ["oTUu82C9Fxo", "Rt1rj9uZPoc", "HFyV-bKlY64", "tXQoFOepbf0"]
    list_of_ids = hf_test_dataset.list_of_ids
    assert list_of_ids[0] == expected_list[0]
    assert list_of_ids[1] == expected_list[1]
    assert list_of_ids[2] == expected_list[2]
    assert list_of_ids[3] == expected_list[3]
    