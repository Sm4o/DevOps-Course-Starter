Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.provision "shell", privileged: true, inline: <<-SHELL
    # Installing prerequisites for pyenv
    apt-get update
    apt-get -y install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    # Install pyenv
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv

    # Configuring session-wide shell environment for Pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init --path)"' >> ~/.profile
    source ~/.profile
    
    # Installing Python 3.7.9 with Pyenv and setting it to the new version globally 
    pyenv install 3.7.9
    pyenv global 3.7.9

    # Installing poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
      cd /vagrant
      poetry install
      export `cat .env | grep '^[A-Z]' | sed 's/\r//' | xargs`
      poetry run gunicorn --reload --bind 0.0.0.0:5000 'todo_app.app:create_app()' --daemon --error-logfile gunicorn.log
    "}
  end
end
