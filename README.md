# DevOps Apprenticeship: Project Exercise
[![Build Status](https://app.travis-ci.com/Sm4o/DevOps-Course-Starter.svg?branch=master)](https://app.travis-ci.com/Sm4o/DevOps-Course-Starter)

Flask ToDo App with MongoDB backend and Vagrant for configuration management.

## Environment variables 

Save credentials to `.env` file as shown in `.env.template`:
``` bash
# Flask server configuration.
FLASK_APP=todo_app/app
FLASK_ENV=development
SECRET_KEY=12345

# Mongo DB
DB_CONNECTION=mongodb://fakemongo.com
DATABASE_NAME=fakedb

# Authentication OAuth
GITHUB_CLIENT_ID=abc1234
GITHUB_CLIENT_SECRET=abc1234

# Local only
OAUTHLIB_INSECURE_TRANSPORT=1
```

## System Requirements

### SSH
Make sure you have created SSH keys and are able to use them to [connect to a remote machine](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

The project uses Vagrant to run the To Do app in a virtual machine that encapsulates the development environment in a single configuration file, making it easy to share and launch with a single command, `vagrant up`.

### Hypervisor
Vagrant requires a hypervisor installed on your development machine. Oracle VirtualBox is a free cross-platform hypervisor, or if you are on Windows then Hyper-V is also an option.

- VirtualBox ([installation instructions](https://www.virtualbox.org/manual/ch02.html))
- Hyper-V (Windows only) ([installation instructions](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v))

### Vagrant
We will be using a configuration management tool called Vagrant.

- Download page: vagrantup.com/downloads
- Installation instructions: vagrantup.com/docs/installation

Once you have installed the version appropriate to your system, check you have access to Vagrant in the shell you are using:

``` bash
vagrant --version
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask/WSGI server to set environment variables. This enables things like development mode (which also enables features like hot reloading when you make a file change).

## Running the App in Vagrant

Vagrant uses a declarative configuration file, `Vagrantfile` in the root folder. Vagrant will provision a virtual machine and install all dependencies before starting the app by running the below command:
```bash
$ vagrant up 
```

You should see output similar to the following:
```bash
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'hashicorp/bionic64' version '1.0.282' is up to date...
==> default: Running the TODO app setup script
    default: Running: inline script
    default: Installing dependencies from lock file
    default: No dependencies to install or update
    default: Installing the current project: todo-app (0.1.0) * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

To troubleshoot any errors on the app check the `gunicorn.log`.

# Running the App in Docker
Make sure Docker is installed and you are logged into Docker Hub. The Dockerfile uses multi-stage builds in order to separate the production and development environments.

- Build commands:
``` bash
docker build --target production --tag todo.app:prod .
```
``` bash
docker build --target development --tag todo.app:dev .
```
``` bash
docker build --target test --tag todo.app:test .
```

To run the app:
``` bash
docker run --env-file .env -p 5000:5000 todo.app:prod
```
``` bash
docker run --env-file .env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/srv/todo_app todo.app:dev
```
``` bash
docker run --env-file .env.test --mount type=bind,source="$(pwd)"/todo_app,target=/srv/todo_app todo.app:test tests
docker run --env-file .env --mount type=bind,source="$(pwd)"/todo_app,target=/srv/todo_app todo.app:test tests_e2e
```

To launch the development app easier you can use docker-compose command:
``` bash
docker-compose up -d --build 
```

# Running tests locally

Run Unit and Integration tests:
```bash
$ poetry run pytest tests
```

Run End-To-End tests with Selenium 
```bash
$ poetry run pytest tests_e2e
```
**Note:** Need to have geckodriver in `$PATH` as Selenium tests are automated using Firefox browser.

To run tests individually:
```bash
$ poetry run pytest test_single/test_foo.py
```

# Travis testing
Everytime a pull request is created or updated Travis CI will build the code and run all tests.
To run the E2E tests it needs MongoDB and Docker registry credentials, which are stored as encrypted environment variables in `.travis.yml`

To use Travis CLI you need to login with `travis login --com --github-token <personal-access-token>` which you can generate [here](https://github.com/settings/tokens)

(First time only)
```bash
$ travis encrypt --pro DOCKER_HUB_PASSWORD="example" --add
$ travis encrypt --pro HEROKU_API_KEY="example" --add
$ travis encrypt --pro SECRET_KEY="example" --add
$ travis encrypt --pro DB_CONNECTION="example" --add
```

Make sure to properly escape bash commands.

## Heroku

Also everytime a pull request is created or updated Travis CI will deploy the main branch to production
Live production instance is hosted on Heroku: https://todo-app-corndel.herokuapp.com/

Remember to setup some heroku environment variables too

(First time only)
``` bash
heroku config:set `cat .env | grep SECRET_KEY`
heroku config:set `cat .env | grep DB_CONNECTION`
heroku config:set `cat .env | grep DATABASE_NAME`
heroku config:set GITHUB_CLIENT_ID=abc1234  # Production app for heroku, not dev
heroku config:set GITHUB_CLIENT_SECRET=abc1234  # Production app for heroku, not dev
```

## OAuth App setup (First time only)

We're using GitHub as OAuth provider. Follow the [documentation](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) to create your OAuth app.

* For the homepage URL field enter the address for accessing the website locally. 
* For the callback add a particular path to this URL for example /login/ callback.

> You will need both a `client-id` and `client-secret` for your .env file. The client-secret once generated will only be shown once, so take a note of it to avoid needing to regenerate one later.