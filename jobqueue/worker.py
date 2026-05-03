
import os
from redis import Redis
from rq import Queue
from jobqueue.jobs.scan_job import run_scan

def enqueue_scan():
    redis_conn = Redis(
        host=os.getenv("REDIS_HOST","localhost"),
        port=6379
    )

    q = Queue(connection=redis_conn)
    q.enqueue(run_scan)
