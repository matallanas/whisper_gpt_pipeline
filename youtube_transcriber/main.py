import math
import os
import argparse
import sqlite3

from datasets import Dataset

from youtube_transcriber.storing.createdb import create_db
from youtube_transcriber.preprocessing.youtubevideopreprocessor import YoutubeVideoPreprocessor
from youtube_transcriber.loading.serialization import JsonSerializer
from youtube_transcriber.utils import nest_list
from youtube_transcriber.datapipeline import create_hardcoded_data_pipeline
from youtube_transcriber.threadeddatapipeline import ThreadedDataPipeline

NUM_THREADS = 2

def parse_args():
    parser = argparse.ArgumentParser(usage="[arguments] --channel_name --num_videos",
                                     description="Program to transcribe YouTube videos.")
    parser.add_argument("--channel_name", 
                        type=str, 
                        required=True,
                        help="Name of the channel from where the videos will be transcribed")
    parser.add_argument("--num_videos", 
                        type=int, 
                        required=True,
                        help="Number of videos to transcribe from --channel_name")
    args = parser.parse_args()
    return args

def main():
    inputs = parse_args()
    create_db("test.db")
    
    # Create necessary resources
    yt_video_processor = YoutubeVideoPreprocessor(mode="channel_name",
                                                  serializer=JsonSerializer()) # TODO: Let user select serializer
    paths = yt_video_processor.preprocess(inputs.channel_name,
                                          inputs.num_videos)
    nested_listed_length = math.ceil(len(paths) / NUM_THREADS)
    nested_paths = nest_list(paths, nested_listed_length)
    data_pipelines = [create_hardcoded_data_pipeline() for i in range(NUM_THREADS)]
    
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
    
    # TODO: Let users define the hf_data_identifier
    hf_dataset_identifier = "Whispering-GPT/test_whisper"
    
    dataset = Dataset.from_sql("SELECT CHANNEL_NAME, URL, TITLE, DESCRIPTION, TRANSCRIPTION, SEGMENTS FROM VIDEO", connection)
    
    dataset.push_to_hub(hf_dataset_identifier)
    
    # Remove db
    os.remove("test.db")

if __name__=="__main__":
    main()