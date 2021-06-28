# DevOps Apprenticeship: Project Exercise
Flask ToDo App with Trello backend and Vagrant for configuration management.

## Trello Setup
To store ToDo items, the project uses as Trello's REST API. To set it up:

1. Create a [Trello account](https://trello.com/signup)

2. Generate an API Key and Token [here](https://trello.com/app-key)

3. Save credentials to `.env` file as shown in `.env.template`:
    ```
    # Flask server configuration.
    FLASK_APP=todo_app/app
    FLASK_ENV=development

    # Trello REST API credentials
    APP_KEY=...
    TOKEN=...
    BOARD_ID=....
    ```

## System Requirements

### SSH
Make sure you have created SSH keys and are able to use them to [connect to a remote machine](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

The project uses Vagrant to run the To Do app in a virtual machine that encapsulates the development environment in a single configuration file, making it easy to share and launch with a single command, `vagrant up`. To prepare your system, ensure you have an official distribution of Python version 3.7+. 

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

## Running the App

Vagrant uses a declarative configuration file, `Vagrantfile` in the root folder. Vagrant will provision a virtual machine and install all dependencies before starting the app by running the below command:
```bash
$ vagrant up 
```

You should see output similar to the following:
```bash
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'hashicorp/bionic64' version '1.0.282' is up to date...
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 5000 (guest) => 5000 (host) (adapter 1)
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: The guest additions on this VM do not match the installed version of
    default: VirtualBox! In most cases this is fine, but in rare cases it can
    default: prevent things such as shared folders from working properly. If you see
    default: shared folder errors, please make sure the guest additions within the
    default: virtual machine match the version of VirtualBox you have installed on
    default: your host and reload your VM.
    default: 
    default: Guest Additions Version: 6.0.10
    default: VirtualBox Version: 6.1
==> default: Mounting shared folders...
    default: /vagrant => /Users/mktszp/Documents/Corndel/projects/DevOps-Course-Starter
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.
==> default: Running action triggers after up ...
==> default: Running trigger: Launching App...
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

# Running tests

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