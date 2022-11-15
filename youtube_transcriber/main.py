import math
import os
import argparse
import sqlite3
import shutil

from datasets import Dataset, concatenate_datasets, load_dataset

from youtube_transcriber.storing.createdb import create_db
from youtube_transcriber.preprocessing.youtubevideopreprocessor import YoutubeVideoPreprocessor
from youtube_transcriber.loading.serialization import JsonSerializer
from youtube_transcriber.utils import nest_list
from youtube_transcriber.datapipeline import create_hardcoded_data_pipeline
from youtube_transcriber.threadeddatapipeline import ThreadedDataPipeline
from youtube_transcriber.dataset.hf_dataset import HFDataset

NUM_THREADS = 2

def numvideos_type(x):
    x = int(x)
    if x > 12:
        raise argparse.ArgumentTypeError("Maximum number of videos is 12")
    if x < 1:
        raise argparse.ArgumentTypeError("Minimum number of videos is 12")
    return x

def parse_args():
    parser = argparse.ArgumentParser(usage="[arguments] --channel_name --num_videos",
                                     description="Program to transcribe YouTube videos.")
    parser.add_argument("--channel_name", 
                        type=str, 
                        required=True,
                        help="Name of the channel from where the videos will be transcribed")
    parser.add_argument("--num_videos", 
                        type=numvideos_type, 
                        required=True,
                        help="Number of videos (min. 1 - max. 12) to transcribe from --channel_name")
    parser.add_argument("--hf_token", 
                        type=str, 
                        required=True,
                        help="Token of your HF account. You need a HF account to upload the dataset")
    parser.add_argument("--hf_dataset_identifier", 
                        type=str, 
                        required=True,
                        help="The ID of the repository to push to in the following format: <user>/<dataset_name> or <org>/<dataset_name>. Also accepts <dataset_name>, which will default to the namespace of the logged-in user.")
    parser.add_argument("--whisper_model", 
                        type=str, 
                        required=True,
                        help="Select one of the available whispers models",
                        choices=["tiny", "base", "small", "medium", "large"])
    
    args = parser.parse_args()
    return args

def main():
    inputs = parse_args()
    create_db("test.db")
    
    # Create necessary resources
    yt_video_processor = YoutubeVideoPreprocessor(mode="channel_name",
                                                  serializer=JsonSerializer()) # TODO: Let user select serializer
    
    hf_dataset = HFDataset(inputs.hf_dataset_identifier)
    videos_downloaded = hf_dataset.list_of_ids
    
    paths, dataset_folder = yt_video_processor.preprocess(inputs.channel_name,
                                                          inputs.num_videos,
                                                          videos_downloaded)
    nested_listed_length = math.ceil(len(paths) / NUM_THREADS)
    nested_paths = nest_list(paths, nested_listed_length)
    data_pipelines = [create_hardcoded_data_pipeline(inputs.whisper_model) for i in range(NUM_THREADS)]
    
    # Run pipelines in multiple threads
    threads = []
    for data_pipeline, thread_paths in zip(data_pipelines, nested_paths):
        threads.append(ThreadedDataPipeline(data_pipeline, thread_paths))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    # Fetch entries and print them
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute("SELECT CHANNEL_NAME, URL, TITLE, DESCRIPTION, TRANSCRIPTION, SEGMENTS FROM VIDEO")
    videos = cursor.fetchall()
    
    print(len(videos))
    
    dataset = Dataset.from_sql("SELECT CHANNEL_NAME, URL, TITLE, DESCRIPTION, TRANSCRIPTION, SEGMENTS FROM VIDEO", connection)
    
    if (hf_dataset.exist==True) and (hf_dataset.is_empty==False):
        dataset_to_upload = concatenate_datasets([hf_dataset.dataset["train"], dataset])
    else:
        dataset_to_upload = dataset
    
    dataset_to_upload.push_to_hub(inputs.hf_dataset_identifier, token=inputs.hf_token)
    
    # Remove db
    os.remove("test.db")
    try:
        shutil.rmtree(dataset_folder)
    except OSError as e:
        print("Error: %s : %s" % (dataset_folder, e.strerror))

if __name__=="__main__":
    main()