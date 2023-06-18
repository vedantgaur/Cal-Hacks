from hume import HumeBatchClient
from hume.models.config import LanguageConfig, FaceConfig
from hume import HumeStreamClient
import os
from typing import Any, Dict, List, Iterator
from base64 import b64encode
from io import BytesIO
from pathlib import Path


def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    for emotion in ["Joy", "Sadness", "Anger"]:
        print(f"- {emotion}: {emotion_map[emotion]:4f}")

def print_sentiment(sentiment: List[Dict[str, Any]]) -> None:
    sentiment_map = {e["name"]: e["score"] for e in sentiment}
    for rating in range(1, 10):
        print(f"- Sentiment {rating}: {sentiment_map[str(rating)]:4f}")

def start_audio_sentiment_analysis_job(file_path):
    client = HumeBatchClient(os.getenv("HUME_API_KEY"))
    # urls = ["https://storage.googleapis.com/hume-test-data/text/happy.txt"]
    # webm_file = file_path
    # mp3_file = os.system(f'ffmpeg -i "{webm_file}" -vn -ab 128k -ar 44100 -y "{webm_file[:-5]}.mp3";')
    files = [file_path[:-5] + ".mp3"]
    
    config = LanguageConfig(sentiment={}, granularity="sentence")
    job = client.submit_job([], [config], files=files)
    
    print("Running...", job)

    job.await_complete()
    print("Job completed with status: ", job.get_predictions())
    return job

def start_face_sentiment_analysis_job(file_path):
    client = HumeBatchClient(os.getenv("HUME_API_KEY"))

    files = [file_path]
    config = FaceConfig(facs={}, fps_pred=3, identify_faces=False, descriptions={})
    job = client.submit_job([], [config], files=files)

    print("Running...", job)
    job.await_complete()
    print("Job completed with status: ", job.get_status())
    return job


def get_job_predictions(job, model): #model = "language" for audio, "face" for video
    full_predictions = job.get_predictions()
    transcription = ""
    print(full_predictions)
    for source in full_predictions:
        # source_name = source["source"]["url"]
        predictions = source["results"]["predictions"]
        for prediction in predictions:
            language_predictions = prediction["models"][model]["grouped_predictions"]
            for language_prediction in language_predictions:
                for chunk in language_prediction["predictions"]:
                    if model=='language':
                        transcription += f" {chunk['text']}"
                        print(chunk["text"])
                        print_emotions(chunk["emotions"])
                        print("~ ~ ~")
                        print_sentiment(chunk["sentiment"])
                        print()
    print(transcription)

def start_sentiment_analysis_job(file_path):
    
    job = start_audio_sentiment_analysis_job(file_path)
    get_job_predictions(job, "language")

    job = start_face_sentiment_analysis_job(file_path)
    get_job_predictions(job, "face")



start_sentiment_analysis_job("src/Backend/temp_bin/react-webcam-stream-capture.webm")