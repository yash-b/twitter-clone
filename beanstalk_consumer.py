import greenstalk
import json
import time
import traceback

# Should return True if job is complete and should be deleted from beanstalk queue.
def handle_post(job):
    print ("Processing async post job")
    pass

def process_jobs():
    print ("Starting beanstalk consumer")
    while (True):
        # Wrap the client getter in a try/catch so that in the case
        # of exceptions we can recreate the client and continue working.
        try:
            # sleep in case of client creation failing constantly
            time.sleep(1)
            with greenstalk.Client(('127.0.0.1', 11300)) as client:
                while True:
                    job_obj = client.reserve() # blocks indefinitely and waits for a job
                    job = json.loads(job_obj.body)
                    job_type = job["beanstalk_consumer_type"]
                    res = False
                    if job_type == "post":
                        res = handle_post(job)
                    else:
                        print ("Unknown job type found: " + job_type)
                        res = True
                    if res:
                        client.delete(job_obj)
            
        except Exception as e:
            print ("beanstalk consumer saw an exception:")
            print (e)
            print(traceback.format_exc())


if __name__ == '__main__':
    process_jobs()