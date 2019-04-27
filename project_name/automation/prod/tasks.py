import json

from invoke import task, run
from beauty_ocean.droplet.entry import create_droplet


def create_the_droplet(token):
    """
    Creates a DigitalOcean droplet and after finishing, returns
    a JSON response with the droplet's data.

    :param str token: the Digital Ocean API token
    :return: a json response
    """
    return create_droplet(token=token)


def get_ip_address(droplet_data):
    """
    Given DigitalOcean's response when the droplet created, return
    the IP address.
    :param str droplet_data: JSON string
    :return: str
    """
    data = json.loads(droplet_data)
    return data["ip_address"]


def edit_hosts(ip_address):
    """
    Given a str (the IP address), open the "hosts" file (in the same
    directory) and edit it in the appropriate format for Ansible to read.
    :param ip_address:
    :return:
    """
    with open('hosts', 'w+') as f:
        f.write('[constants]\n')
        f.write(ip_address)


def droplet_birth(step=False):
    """
    Runs Ansible on the remote host machine and performs the basic
    configuration (installs Python, creates user, removes ssh root access)
    :param c:
    :param bool step: whether or not to run ansible command per step
    :return: None
    """
    s = "--step" if step else ""
    command = f"ansible-playbook {s} deploy_root.yml"
    while True:
        res = run(command, pty=True, warn=True)
        if res.exited in [0, 99]: break


def droplet_adult(step=False):
    """
    Runs Ansible on the remote machine and performs setup configuration
    such as installing Nginx, Postgres, pyenv, uwsgi and the app itself.
    :param c:
    :param bool step: whether or not to run ansible command per step
    :return: None
    """
    # -K prompts for remote host user's sudo password
    s = "--step" if step else ""
    command = f"ansible-playbook -K {s} deploy_user.yml"
    while True:
        res = run(command, pty=True, warn=True)
        if res.exited in [0, 99]: break


@task
def deploy(c, step=False, token=None):
    """
    Deploy the current app to Digital Ocean. It automatically creates the
    droplet, setup the server and deploy the app.

    Assumes the app is already pushed at BitBucket. Later, in an Ansible
    action, you'll be asked to paste remote host's (droplet's) public key
    to the app's BitBucket repo ssh "Access keys". That's a feature that
    BitBucket API v1 had, but in v2 have removed. Thus, this procedure must
    be done manually.

    :param c:
    :param str token: the Digital Ocean API token
    :param bool step: whether or not to run ansible command per step
    :return:
    """
    res = create_the_droplet(token=token)
    ip = get_ip_address(droplet_data=res)
    edit_hosts(ip_address=ip)
    droplet_birth(step=step)
    droplet_adult(step=step)
