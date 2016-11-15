from rq import Connection
from rq import Queue, worker
from rq.job import JobStatus
from settings import max_retry_count, download_queue


def retry_handler(job, exc_type, exc_value, traceback):
    print("" * 100 + "retrying")
    job.meta.setdefault('failures', 1)
    job.meta['failures'] += 1
    print("failed :::: %d" % (job.meta['failures'],))
    if job.meta['failures'] > max_retry_count or isinstance(exc_type, (LookupError,)):
        job.save()
        return True

    #import pdb; pdb.set_trace()
    job.status = JobStatus.QUEUED
    with Connection():
        queue = Queue(job.origin)
        queue.enqueue_job(job)

    return False  # Job is handled. Stop the handler chain.


