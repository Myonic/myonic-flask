Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.provision "shell", inline: <<-SHELL
    echo "--INSTALLING PYTHON--"
    apt-get update
    apt-get install -y python-pip python-dev build-essential python-imaging
    export FLASK_APP=/vagrant/myonic/__init__.py
    export FLASK_DEBUG=1
    echo "--SETTING BASH PROFILE--"
    rm /etc/profile
    echo "# /etc/profile: system-wide .profile file for the Bourne shell (sh(1))
# and Bourne compatible shells (bash(1), ksh(1), ash(1), ...).

if [ "$PS1" ]; then
  if [ "$BASH" ] && [ "$BASH" != "/bin/sh" ]; then
    # The file bash.bashrc already sets the default PS1.
    # PS1='\h:\w\$ '
    if [ -f /etc/bash.bashrc ]; then
      . /etc/bash.bashrc
    fi
  else
    if [ "`id -u`" -eq 0 ]; then
      PS1='# '
    else
      PS1='$ '
    fi
  fi
fi

# The default umask is now handled by pam_umask.
# See pam_umask(8) and /etc/login.defs.

if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/*.sh; do
    if [ -r $i ]; then
      . $i
    fi
  done
  unset i
fi" >> /etc/profile
    echo "export FLASK_APP=/vagrant/myonic/__init__.py" >> /etc/profile
    echo "export FLASK_DEBUG=1" >> /etc/profile
    echo "export OAUTHLIB_INSECURE_TRANSPORT=1" >> /etc/profile
    echo "export OAUTHLIB_RELAX_TOKEN_SCOPE=1" >> /etc/profile
    echo "export SECRET_KEY='test_key'" >> /etc/profile
    echo "cd /vagrant/myonic" >> /etc/profile
    echo "echo Remember to include the host when starting Flask: \"flask run --host=0.0.0.0\"" >> /etc/profile
    cat /etc/profile
    echo "--INSTALLING REQUIREMENTS--"
    pip install -r /vagrant/requirements.txt
    flask db migrate
    flask db upgrade
    echo "
    !!!--------------------------------------------------------------------------------------------------------!!!
    !!!--REMEMBER: This Vagrant enviroment is for development use ONLY and should NEVER be used in production.--!!
    !!!--------------------------------------------------------------------------------------------------------!!!
    "
  SHELL
end
