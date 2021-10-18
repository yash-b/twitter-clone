# add timeline python code here

"""First hug API (local, command-line, and HTTP access)"""
import hug


@hug.cli()
@hug.get(examples='userTimeline')
@hug.local()

# not sure what to put inside of the function 
def user_timeline():
    return {"success":True}

def home_timeline():
    return {"success":True}

def public_timeline():
    return {"success":True}

if __name__ == '__main__':
    user_timeline.interface.cli()
    home_timeline.interface.cli()
    public_timeline.interface.cli()

#setting up a new port other than 8000
hug.API(__name__).http.serve(port=8005)