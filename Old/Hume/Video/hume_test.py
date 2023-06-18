import hume
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from pprint import pprint
import os

client = HumeBatchClient(os.environ("HUME_API_KEY"))
urls = ["https://iep.utm.edu/wp-content/media/hume-bust.jpg"]
config = FaceConfig()
job = client.submit_job(urls, [config])
print(job)

status = job.get_status()
print(f"Job status: {status}")

# details = job.get_details()
# run_time_ms = details.get_run_time_ms()
# print(f"Job ran for {run_time_ms} milliseconds")

# predictions = job.get_predictions()
# pprint(predictions)