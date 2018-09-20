# GENERAL

This project structure is in active development and continuously evolves. It utilizes: 

- The batteries-included super-fast template [Jinja2](http://jinja.pocoo.org/docs/latest/).
- The wrapper around it (to make our lives easier) [django-jinja](https://niwinz.github.io/django-jinja/latest/).
- The command-like tool [Invoke](http://docs.pyinvoke.org/en/latest/).
- The IT automation tool [Ansible](http://docs.ansible.com/ansible/latest/index.html).
- The CLI command for expoiting DigitalOcean API [beauty-ocean](https://beauty-ocean.readthedocs.io/en/latest/).
- [Requests](http://www.python-requests.org/en/master/) to make our lives easier.
- The package management tool, [pipenv](https://docs.pipenv.org/). A `Pipfile` is already included with sane defaults.
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) to parse ``yaml`` files.

Before run `pipenv install --dev`, have a look in the file and add/remove (Django) packages according to your needs.


# OBJECTIVE

This Django skeleton tries to handle the most boilerplate for you (me) in order to facilitate the deployment procedure.
When we say deployment, we mean [DigitalOcean](https://www.digitalocean.com). I do not work for them, nor I get paid by them. I just love their
services, VPS pricing plans and UX. That's all. I have tried [Linode](https://www.linode.com) too, but no luck there. That's just personal preference.

Before running the usual command `django-admin startproject project_name` (in order to create your brand new Django project),
try running the following command instead:

    django-admin startproject --template https://github.com/manikos/cc_do/archive/master.zip --extension py,json,html --name constants.yml,gitignore project_name

When the command completes, you'll have a project structure which is (almost) deployment ready. Read below for more information.


# INSTALLATION

## First part (development)

(HINT): Create a virtualenv (i.e ``django_env``) which will be used only for Django-specific commands (like ``django-admin``) and install ``django`` inside it: ``$ mkvirtualenv -p $(which python3.6) django_env``.
(HINT): Maybe take a look at [pyenv](https://github.com/pyenv/pyenv)).

1. Ensure that you have `pipenv` installed to your machine. If not, install it: `$ pip install --user pipenv` (never use sudo)
2. Activate the previously created ``django_env``: `$ workon django_env` and ``$ cd path/to/projects/dir``
3. Create the project skeleton `(django_env)$ django-admin startproject --template https://github.com/manikos/cc_do/archive/master.zip --extension py,json,html --name constants.yml,gitignore project_name`
4. Deactivate ``django_env`` (job's done): ``(django_env)$ deactivate``
4. Take a look at the `Pipfile` and remove any dependencies according to your needs.
5. Install dependencies (including dev-packages) `$ cd /path/to/project/ && pipenv install --dev`.
6. Activate the virtualenv in order not to do ``pipenv run <command>`` and instead do ``<command>``, ``$ pipenv shell``.
6. ``(project-<hash>)$ cd path/to/automation/dev && inv --list``, it will list all available (dev) commands to create a BitBucket private repo and/or a PostgreSQL local database.

Take a look at `automation/dev/tasks.py` for some useful commands to get you started. Also, take a look at the `TODO: ` sections spread accross the skeleton 
and tweak values according to your needs.


## Second part (deployment)

1. Ensure that you have looked the values to be changed at `automation/prod/group_vars/all/constants.yml`.
2. Ensure that you have provided a `automation/prod/group_vars/all/vault.yml` file which is encrypted using 
[ansible-vault](https://docs.ansible.com/ansible/2.4/vault.html#creating-encrypted-files) command.
    - This file is a `yml` file.
    - Must contain the below keys:

    | Keys              | Description |
    | ----------------- |-------------|
    | `user_group`      | user's group (usually same as `user_name`) |
    | `user_name`       | user's username |
    | `user_salt`       | a random string of up to 8 characters [a-zA-Z0-9./] |
    | `user_pwd`        | user's password (used for `sudo` commands) |
    | `user_comment`    | user's full name (optional) |
    | `bb_user`         | your bitbucket username |
    | `bb_pwd`          | your bitbucket password |
    | `db_user`         | production postgres database user (usually the same a `user_name`) |
    | `db_pwd`          | production postgres database password |
    
    For example, a `vault.yml` file could look like this:
    
        ---
        
        user_group: mike
        user_name: mike
        user_salt: aThko86z
        user_pwd: mikeSudoPassword
        user_comment: Mike Michael
        bb_user: mike
        bb_pwd: mikeBitBucketPwd
        db_user: mike
        db_pwd: mikePostgresPwd
            
    - Usually, you want the same values for every project you deploy, in order not to get lost when you must `ssh` in the server. So, create this `vault.yml` file once 
    and then forget about it. **Just don't forget the password in case you have to edit/view `vault.yml`**!
  
3. To deploy the project on DigitalOcean `(venv)$ cd path/to/project/automation/prod && inv deploy`. Done!



# STRUCTURE

The produced project structure looks like this:

<pre>
.
├── dtl_utils
│   ├── apps.py
│   ├── __init__.py
│   └── templatetags
│       ├── dtl_tags.py
│       └── __init__.py
├── gitignore
├── logs
│   ├── db.log
│   ├── dev.log
│   ├── my_apps.log
│   └── production.log
├── manage.py
├── media_root
│   └── README.md
├── Pipfile
├── project_name
│   ├── automation
│   │   ├── dev
│   │   │   └── tasks.py
│   │   └── prod
│   │       ├── ansible.cfg
│   │       ├── deploy_root.yml
│   │       ├── deploy_user.yml
│   │       ├── filter_plugins
│   │       │   └── db_filters.py
│   │       ├── group_vars
│   │       │   └── all
│   │       │       └── constants.yml
│   │       ├── hosts
│   │       ├── README.md
│   │       ├── roles
│   │       │   ├── manikos.app
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.birth
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.bitbucket
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.common
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   │   └── vimrc
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   │   └── bash_aliases.j2
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.django
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.fail2ban
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   │   └── jail.local.j2
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.nginx
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   │   ├── nginx.conf.j2
│   │       │   │   │   └── nginx_sites_avail.j2
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.pipenv
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.postgres
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.pyenv
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   │   └── pyenvrc.j2
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   ├── manikos.ufw
│   │       │   │   ├── defaults
│   │       │   │   │   └── main.yml
│   │       │   │   ├── files
│   │       │   │   ├── handlers
│   │       │   │   │   └── main.yml
│   │       │   │   ├── meta
│   │       │   │   │   └── main.yml
│   │       │   │   ├── README.md
│   │       │   │   ├── tasks
│   │       │   │   │   └── main.yml
│   │       │   │   ├── templates
│   │       │   │   ├── tests
│   │       │   │   │   ├── inventory
│   │       │   │   │   └── test.yml
│   │       │   │   └── vars
│   │       │   │       └── main.yml
│   │       │   └── manikos.uwsgi
│   │       │       ├── defaults
│   │       │       │   └── main.yml
│   │       │       ├── files
│   │       │       ├── handlers
│   │       │       │   └── main.yml
│   │       │       ├── meta
│   │       │       │   └── main.yml
│   │       │       ├── README.md
│   │       │       ├── tasks
│   │       │       │   └── main.yml
│   │       │       ├── templates
│   │       │       │   ├── uwsgi.ini.j2
│   │       │       │   └── uwsgi.service.j2
│   │       │       ├── tests
│   │       │       │   ├── inventory
│   │       │       │   └── test.yml
│   │       │       └── vars
│   │       │           └── main.yml
│   │       └── tasks.py
│   ├── __init__.py
│   ├── jinja2
│   │   ├── filters.py
│   │   ├── __init__.py
│   │   └── methods.py
│   ├── locale
│   │   └── el
│   │       └── LC_MESSAGES
│   │           └── README.md
│   ├── settings
│   │   ├── base.py
│   │   ├── __init__.py
│   │   ├── local.py
│   │   ├── prod.py
│   │   └── secret.json
│   ├── sitemap.py
│   ├── urls.py
│   └── wsgi.py
├── READ_ME
├── README.md
├── robots.txt
├── static
│   ├── css
│   │   └── style.css
│   ├── fonts
│   │   └── font.ttf
│   ├── img
│   │   ├── empty.png
│   │   └── favicons
│   │       └── favicon.ico
│   ├── js
│   │   ├── adminPreviewImage.js
│   │   └── main.js
│   └── src
│       └── various_original_files
├── static_root
│   └── README.md
└── templates
    ├── admin
    │   ├── base_site.html
    │   └── change_form.html
    ├── base
    │   ├── base.html
    │   └── index.html
    └── sitemap
        └── sitemap.xml

137 directories, 154 files

</pre>


# TO DO

The next thing I like to build is a [docker](https://www.docker.com/)-ready fully functional website skeleton, batteries included.

