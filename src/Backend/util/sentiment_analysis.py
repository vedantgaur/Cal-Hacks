from hume import HumeBatchClient
from hume.models.config import LanguageConfig
from hume import HumeBatchClient, TranscriptionConfig
from hume.models.config import ProsodyConfig
import os
from typing import Any, Dict, List


def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    for emotion in ["Joy", "Sadness", "Anger"]:
        print(f"- {emotion}: {emotion_map[emotion]:4f}")

def print_sentiment(sentiment: List[Dict[str, Any]]) -> None:
    sentiment_map = {e["name"]: e["score"] for e in sentiment}
    for rating in range(1, 10):
        print(f"- Sentiment {rating}: {sentiment_map[str(rating)]:4f}")

def start_sentiment_analysis_job():
    client = HumeBatchClient(os.getenv("HUME_API_KEY"))
    # urls = ["https://storage.googleapis.com/hume-test-data/text/happy.txt"]
    files = ["src/Backend/audio/hi.mp3"]
    config = LanguageConfig(sentiment={})
    job = client.submit_job([], [config], files=files)
    
    print("Running...", job)

    job.await_complete()
    print("Job completed with status: ", job.get_status())
    return job

def get_job_predictions(job):
    full_predictions = job.get_predictions()
    transcription = ""
    print(full_predictions)
    for source in full_predictions:
        # source_name = source["source"]["url"]
        predictions = source["results"]["predictions"]
        for prediction in predictions:
            language_predictions = prediction["models"]["language"]["grouped_predictions"]
            for language_prediction in language_predictions:
                for chunk in language_prediction["predictions"]:
                    print(chunk["text"])
                    transcription += f" {chunk['text']}"
                    print_emotions(chunk["emotions"])
                    print("~ ~ ~")
                    print_sentiment(chunk["sentiment"])
                    print()
    print(transcription)

job = start_sentiment_analysis_job()
get_job_predictions(job)