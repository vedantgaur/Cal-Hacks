import os
from hume import HumeBatchClient
from hume.models.config import FaceConfig

api_key = os.getenv("HUME_API_KEY")
# print(api_key)

client = HumeBatchClient(api_key)
urls = ["https://iep.utm.edu/wp-content/media/hume-bust.jpg"]
config = FaceConfig()
job = client.submit_job(urls, [config])

status = job.get_status()
print(f"Job status: {status}")

details = job.get_details()
run_time_ms = details.get_run_time_ms()
print(f"Job ran for {run_time_ms} milliseconds")
