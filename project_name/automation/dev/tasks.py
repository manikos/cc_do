"""
Invoke file for:

+ Project git init
    - BitBucket repo creation
    - Git push to origin master
+ Creation of the local PostgreSQL project database.

$ mkvirtualenv -p $(which python3.6) venv
(venv)$ pip install invoke requests pyyaml
(venv)$ cd project/automation/dev
(venv)$ inv pg
(venv)$ inv git --create
"""
import sys
import os
import contextlib
from getpass import getpass

import yaml
import requests
from invoke import task, run
from invoke.exceptions import Failure

PROMPT = "-->"


@contextlib.contextmanager
def chdir(dir_name=""):
    """
    Simple context manager for switching to a different dir temporarily

    :param str dir_name: the directory to change to
    :return: None
    """
    current_dir = os.getcwd()
    try:
        if dir_name:
            os.chdir(dir_name)
        yield
    finally:
        os.chdir(current_dir)


def get_user_name():
    """Get bitbucket user name"""
    usr = ""  # TODO: Add bitbucket username here (if you like)
    while not usr:
        usr = input(f"Enter your BitBucket username{PROMPT} ")
    return usr


def get_user_pwd():
    """Get bitbucket user password"""
    bb_pwd = ""
    while not bb_pwd:
        bb_pwd = getpass(f"Enter bitbucket password{PROMPT} ")
    return bb_pwd


def get_repo_name():
    """Get APP name which will be used for the repo name as well"""
    with open("../prod/group_vars/all/constants.yml", "r") as f:
        obj = yaml.load(f, Loader=yaml.FullLoader)
        try:
            app_name = obj["APP"]
        except KeyError:
            err = "No 'APP' key found inside 'constants.yml file!"
            raise ValueError(err) from None
        else:
            return app_name


def usr_repo():
    """
    Collects data from the "constants.yml" file which will be needed to
    create the repository.
    :return: dict
    """
    return {
        "bb_usr": get_user_name(),
        "bb_repo": get_repo_name(),
    }


def build_url(bb_usr, bb_repo):
    """
    Given a username + repo name return the BitBucket REST API v2 url for
    that repository.

    :param str bb_usr: BitBucket username
    :param str bb_repo: BitBucket repository name
    :return: string
    """
    return f"https://api.bitbucket.org/2.0/repositories/{bb_usr}/{bb_repo}"


def create_repo(bb_usr, bb_pwd, bb_repo):
    """
    Create the repository if repo not already exists.

    :param str bb_usr: BitBucket username
    :param str bb_pwd: BitBucket password
    :param str bb_repo: BitBucket repository name
    :return: None
    """
    url = build_url(bb_usr, bb_repo)
    res = requests.get(url=url, auth=(bb_usr, bb_pwd))
    if res.status_code == 200:
        print(f"Repo '{bb_repo}' already exists! Exiting...")
        sys.exit(0)
    res = requests.post(url=url, auth=(bb_usr, bb_pwd))
    res.raise_for_status()
    print(f"Repo '{bb_repo}' has been created successfully!")


def delete_repo(bb_usr, bb_pwd, bb_repo):
    """
    Delete the repository if repo exists.

    :param str bb_usr: BitBucket username
    :param str bb_pwd: BitBucket password
    :param str bb_repo: BitBucket repository name
    :return: None
    """
    url = build_url(bb_usr, bb_repo)
    res = requests.delete(url=url, auth=(bb_usr, bb_pwd))
    if res.status_code == 204:
        print(f"Repo '{bb_repo}' has been deleted successfully!")
    elif res.status_code == 404:
        print(f"Repo '{bb_repo}' does not exist!")


def git_init_push(bb_usr, bb_repo):
    """
    Initialize the APP under git version control system and pushes all files
    to master branch.
    :return: None
    """
    ssh_url = f"ssh://git@bitbucket.org/{bb_usr}/{bb_repo}.git"
    with chdir("../../.."):  # go up 3 times, to be in the project root
        run("git init")
        run("git add --all")

        run("git remote add origin {}".format(ssh_url))
        run('git commit -m "Initial commit"')

        run("git push -u origin master")
    print("Push successful :)")


@task
def git(c, create=False, delete=False):
    """
    Entry point for basic repo handling (creation/deletion).

    inv git --create (will create the repo)
    inv git --delete (will delete the repo)
    inv git --create --delete (will create and then delete the repo)
    """
    data = usr_repo()
    bb_usr = data["bb_usr"]
    bb_repo = data["bb_repo"]
    bb_pwd = get_user_pwd()

    if create:
        create_repo(bb_usr, bb_pwd, bb_repo)
        git_init_push(bb_usr, bb_repo)

    if delete:
        delete_repo(bb_usr, bb_pwd, bb_repo)


def install_required_packages():
    """
    Prompts the user to confirm installation of required PostgreSQL system
    packages.
    :return: None
    """
    confirm = input(f"Install required packages [y, N]{PROMPT} ") or "n"
    if confirm == "n":
        return
    if confirm == "y":
        postgres_packages = [
            "postgresql", "libpq-dev", "python3-psycopg2",
            "postgresql-client-common",
            "postgresql-client", "postgresql-contrib", "pgadmin3",
        ]
        run("sudo apt-get update > /dev/null")
        run("sudo apt-get install -y {}".format(" ".join(postgres_packages)))
        print(f"Packages installed successfully!")


def create_pg_user(user_name):
    """
    Given a user name, create a PostgreSQL NOSUPERUSER user.

    :param str user_name: The database user name
    :return: None
    """
    user_exists = run(f'psql postgres -tAc "SELECT 1 FROM pg_roles WHERE '
                      f'rolname=\'{user_name}\'"', hide="both")
    # if user is found, stdout will be 1 (None otherwise)
    if not user_exists.stdout:
        # -d: env.db_owner can create new databases
        # -E: env.db_owner's given password will be stored as a hashed value,
        # instead of plain text
        # Development dummy default password:
        #   123456 --hashed--> md575bd30c0d7a5d43d28f465a53cc8c340
        # The following CREATE ROLE command is identical to this IF given
        # password is 123456:
        #   "sudo -u postgres createuser -d -E -P {}".format(env.db_owner)
        run(f'sudo -u postgres psql -c "CREATE ROLE {user_name} ENCRYPTED '
            'PASSWORD \'md575bd30c0d7a5d43d28f465a53cc8c340\' NOSUPERUSER '
            'CREATEDB NOCREATEROLE INHERIT LOGIN;"')
        print(f"User {user_name} has been created successfully!")
    print(f"User {user_name} already exists!")


def create_db(db_owner):
    """
    Given a user name, create a PostgreSQL database owned by this user.

    :param str db_owner: The database usre name
    :return: None
    """
    db_name = ""
    while not db_name:
        db_name = input(f"Database name{PROMPT} ")
    # -l: list available databases, then exit
    # -q: run quietly (no messages, only query output)
    # -t: print rows only
    try:
        run(f'psql -lqt | cut -d \| -f 1 | grep -w "{db_name}"', hide="out")
    except Failure:
        run(f"createdb {db_name} -O {db_owner}")
        print(f"Database '{db_name}' created successfully!")
    else:
        print(f"Database '{db_name}' already exists!")


@task
def pg(c):
    """
    Installs PostgreSQL required packages and creates the database user
    and the database itself.

    inv pg
    """
    install_required_packages()
    db_owner = ""
    while not db_owner:
        db_owner = input(f"Database owner{PROMPT} ")
    create_pg_user(db_owner)
    create_db(db_owner)

