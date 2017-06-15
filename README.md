# Myonic CMS
A rewrite of the Myonic website in Python/Flask.

## Setup

### Vagrant Development Environment
A very simple and easy way to set up a working consistent environment for developing this software is with [Vagrant](https://www.vagrantup.com/). Vagrant creates virtual machines with a custom configuration. To create the virtual machine for this software, follow the instructions below.

1. Navigate to the myonic-flask directory
2. Run `$ vagrant up` to initialize the virtual machine
3. Run `$ vagrant ssh` to enter the machine

It is that simple. Now you are working in a fully configured development environment for Myonic CMS.

***DO NOT USE IN PRODUCTION***

### Docker
[Docker](https://www.docker.com/) is a container system that makes deploying very simple. By default, the container is configured in production mode but this can be changed with environment variables.

All you need to do to set up a container is `$ docker run myonic/myonic-cms`

---

## Other Stuff
* Run Flask in shell mode: `$ flask shell`
* Database
  * Migrate database: `$ flask db migrate`
  * Upgrade database: `$ flask db upgrade`
  * More database tools: `$ flask db --help`
* Put Flask in debug mode by setting the environment variable `FLASK_DEBUG=1`
* The `SECRET_KEY` environment variable should be set
  * Without Docker, this is required
  * With Docker, this should be changed

*On local development environments, you must set the environment variables `OAUTHLIB_INSECURE_TRANSPORT=1` and `OAUTHLIB_RELAX_TOKEN_SCOPE=1` in order for the Google auth to function properly but* ***DO NOT DO USE IN PRODUCTION***
