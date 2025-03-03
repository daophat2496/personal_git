from google.cloud import pubsub_v1
from datetime import datetime
import json

project = ""
topic = ""

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project, topic)

message = {
    "user_id": 123456,  # INTEGER
    "favorite_brand": f"Test Streaming Dataflow Pipeline {datetime.utcnow().strftime('%Y-%m%d %H:%M:%S')}",  # STRING
    "join_date": "2023-09-12",
    "join_ts": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
}

message_json = json.dumps(message)
message_bytes = message_json.encode('utf-8')

publish_future = publisher.publish(topic_path, message_bytes)
print(f"Message published with ID: {publish_future.result()}")
print(f"Message: {message}")
