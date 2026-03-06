import os
import redis
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("REDIS_HOST")
port = int(os.getenv("REDIS_PORT"))
password = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
    host=host,
    port=port,
    password=password,
    decode_responses=True
)

try:
    success = r.set('test_connection', 'ok')
    result = r.get('test_connection')
    print(f"Connection successful! Result: {result}")
except Exception as e:
    print(f"Connection failed: {e}")

