from hume import HumeBatchClient
from hume.models.config import LanguageConfig, FaceConfig, BurstConfig, ProsodyConfig
from hume import HumeStreamClient
import os
from typing import Any, Dict, List, Iterator
from base64 import b64encode
from io import BytesIO
from pathlib import Path


def get_top_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    # for emotion in emotion_map:
    #     print(f"- {emotion}: {emotion_map[emotion]:4f}")
    sorted_emotion_map = sorted(emotion_map.items(), key=lambda x: x[1], reverse=True)[:3]
    return sorted_emotion_map

def start_audio_sentiment_analysis_job(file_path):
    client = HumeBatchClient(os.getenv("HUME_API_KEY"))
    
    burst_config = BurstConfig()
    prosody_config = ProsodyConfig()

    mp3_file = os.system(f'ffmpeg -i "{file_path}" -vn -ab 128k -ar 44100 -y "{file_path[:-5]}.mp3";')
    files = [file_path[:-5] + ".mp3"]
    
    job = client.submit_job([], [burst_config, prosody_config], files=files)
    print("Running...", job)

    job.await_complete()
    print("Job completed with status: ", job.get_status())
    return job


def start_text_sentiment_analysis_job(file_path):
    client = HumeBatchClient(os.getenv("HUME_API_KEY"))
    mp3_file = os.system(f'ffmpeg -i "{file_path}" -vn -ab 128k -ar 44100 -y "{file_path[:-5]}.mp3";')
    files = [file_path[:-5] + ".mp3"]
    
    config = LanguageConfig(sentiment={}, granularity="utterance")
    job = client.submit_job([], [config], files=files)
    
    print("Running...", job)

    job.await_complete()
    print("Job completed with status: ", job.get_status())
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


def get_job_predictions(job, models): #model = "language" for text, "face" for video, "prosody" + "burst" for audio
    full_predictions = job.get_predictions()
    transcription = ""
    # print(full_predictions)
    for model in models:
        for source in full_predictions:
            # source_name = source["source"]["url"]
            predictions = source["results"]["predictions"]
            for prediction in predictions:
                predictions = prediction["models"][model]["grouped_predictions"]
                for prediction in predictions:
                    for chunk in prediction["predictions"]:
                        if model=='language':
                            transcription += f" {chunk['text']}"
                            # print(chunk["text"])
                        top_emotions = get_top_emotions(chunk["emotions"])
                        if model!='language':
                            return top_emotions
    return (transcription, top_emotions)

def analyze_sentiment(file_path):
    job = start_text_sentiment_analysis_job(file_path)
    language_ouput = get_job_predictions(job, ["language"])
    transcript = language_ouput[0]
    language = language_ouput[1]

    job = start_face_sentiment_analysis_job(file_path)
    face = get_job_predictions(job, ["face"])

    job = start_audio_sentiment_analysis_job(file_path)
    prosody = get_job_predictions(job, ["prosody"])
    burst = get_job_predictions(job, ["burst"])

    return {
       "transcript" : transcript,
       "language" : language,
       "face": face,
       "prosody": prosody,
       "burst": burst
    }