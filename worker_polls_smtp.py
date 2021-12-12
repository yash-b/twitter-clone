import greenstalk
import time
import json
import traceback
import smtplib

# These services mentioned below are automatically started by Foreman.

#Need to configure beanstalk for the address
#Use the command: beanstalkd -l 127.0.0.1 -p 11400

#Need to configure smtp debugger address
#Use this command: python -m smtpd -n -c DebuggingServer localhost:1026

def notifyUserInvalidPollUrl():
    print ("Starting polls email notifying worker")
        # Wrap the client getter in a try/catch so that in the case
        # of exceptions we can recreate the client and continue working.
    with greenstalk.Client(('127.0.0.1', 11400)) as client:
        while True:
            job_obj = client.reserve() # blocks indefinitely and waits for a job
            try:
                job = json.loads(job_obj.body)
                message = job["message"]
                senderEmail = job["sender"]
                receiverEmail = job["receiver"]
                msg = ("From: %s\r\nTo: %s\r\n\r\n"% (senderEmail, receiverEmail)) + message
                server = smtplib.SMTP("localhost", 1026)
                server.set_debuglevel(1)
                server.sendmail(senderEmail, receiverEmail, msg)
                server.quit()
                client.delete(job_obj)
            except Exception as e:
                client.delete(job_obj)
                print ("Polls email notifying worker saw an exception:")
                print (e)
                print(traceback.format_exc())

if __name__ == "__main__":
    notifyUserInvalidPollUrl()