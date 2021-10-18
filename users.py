# Add user python code here
"""First hug API (local, command-line, and HTTP access)"""
import hug


@hug.cli()
@hug.post(examples='CreateUsers')
@hug.local()
def create_user(username: hug.types.text, bio: hug.types.text, email: hug.types.text, password: hug.types.text, hug_timer=3):
    
    return {"success":True}


if __name__ == '__main__':
    create_user.interface.cli()
