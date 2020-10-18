# This is a worker or receiver. It will recives jobs from
# a jobs queue calld 'default' implemented in Redis.
import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == "__main__":
    with Connection(conn):
        Worker = Worker(list(map(Queue, listen)))
        Worker.work()
