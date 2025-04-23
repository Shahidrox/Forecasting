# Document

## python -m venv .venv

To set up a virtual environment for the project, one can use the following command:

```bash
python -m venv .venv
source .venv/bin/activate
```

The first command `python -m venv .venv` creates a new virtual environment named `.venv` for the project directory. The second command `source .venv/bin/activate` activates the virtual environment, allows to install and manage project-specific dependencies.

## pip freeze > requirements.txt

The command `pip freeze > requirements.txt` is used to generate a list of all installed Python packages and their versions, and save it to a file called `requirements.txt`. This file is commonly used to document project dependencies and allows for easy installation of the same set of packages on different environments.

To add a new package to the project, can use the `pip install` command followed by the package name. For example:

```bash
pip install package_name
```

Make sure to activate the virtual environment before running this command to ensure that the package is installed within the project's environment.
To run the project using Docker, you can use the following command:

```bash
docker-compose up -d
```

The `docker-compose up -d` command starts the project's containers in detached mode, allowing them to run in the background. This is useful for running the project as a set of interconnected services.

Make sure you have Docker and Docker Compose installed on your system before running this command. Docker Compose uses a YAML file (usually named `docker-compose.yml`) to define the services, networks, and volumes required for the project.

Once the containers are up and running, you can access the project through the specified ports or endpoints defined in the Docker Compose file.

Remember to stop the containers using the `docker-compose down` command when you're done with the project.


<!-- find . -type d -name "__pycache__" -exec rm -r {} + -->