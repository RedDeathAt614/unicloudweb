from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'ec2-user'
env.key_filename = '~/Documents/Projects/Kollektiv/Amazon/SSH keys/MichaelUnicloud.pem'

env.environment = "staging"

def hello():
    print("Hello world!")

def production():
    env.hosts = ['54.171.241.122']
    env.environment = "production"
    env.codepath = "unicloudtest/unicloud"

def staging():
    env.hosts = ['54.77.215.230']
    env.environment = "staging"
    env.codepath = "unicloudtest/unicloud"

def landing():
    env.hosts = ['54.154.34.182']
    env.environment = "landing"
    env.codepath = "landing/unicloudweb"

def deploy(stop="true"):
    print("")
    print("Deploying to " + env.user + "@" + env.user + " using keyfile:" + env.key_filename)
    with cd(env.codepath):
        with settings(warn_only=True):
            if (stop == "true"):
                print("STOPPING server")
                isStopped = run('sudo forever stop app.js')

                if isStopped.failed and not confirm("Server appears to be already stopped. Continue anyway?"):
                    abort("Aborting at user request")
            gitpull = run('sudo git pull')

            if (gitpull.failed):
                if confirm("Do you want to try and run git stash?"):
                    run('sudo git stash')
                    gitpull = run('sudo git pull')
                if stop=="true" and gitpull.failed:
                    if confirm("Do you want to restart the server?"):
                        run('sudo forever start app.js -o ./out.log -e ./err.log -l ./forever.log')
                    abort("Aborting..")
            run('sudo npm install')
            if (env.environment != "landing"):
                run('sudo bower install --allow-root')

            if (stop == "true"):
                run('sudo forever start app.js -o ./out.log -e ./err.log -l ./forever.log')
            if (env.environment == "production"):
                register_deployment()


def restart():
    print("")
    print("Restarting the server");
    with cd(env.codepath):
        run('sudo forever stop app.js')
        run('sudo forever start app.js -o ./out.log -e ./err.log -l ./forever.log')


def start():
    print("")
    print("starting the server");
    with cd(env.codepath):
        run('sudo forever start app.js -o ./out.log -e ./err.log -l ./forever.log')

def stop():
    print("")
    print("WARNING! STOPPING SERVER - run 'fab restart' to start it again")
    with cd(env.codepath):
        run('sudo forever stop app.js')

def register_deployment():
    path = "./"
    with(lcd(path)):
        local("""
            curl https://opbeat.com/api/v1/organizations/c71b0e1ba317435aad7c429b63a80ec2/apps/5aa3e9a576/releases/ -H "Authorization: Bearer d28c6e7642e1b30722fe32528131fe9818302839" -d rev=`git log -n 1 --pretty=format:%H` -d branch=`git rev-parse --abbrev-ref HEAD` -d status=completed
        """)
