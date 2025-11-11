# Danish Data Science Community - website
Welcome!

## Introduction
This is Danish Data Science Communities internal website repository.
If you are new to the Django webframework please take a look at the [Django documentation](https://www.djangoproject.com)

### - Installing dependencies (Linux/MacOs)

#### Option 1: Using pyproject.toml (Recommended)
The project now uses `pyproject.toml` for modern Python package management.
While positioned in the root folder, run the following commands:

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -e .
```

To install with development dependencies:
```bash
pip install -e ".[dev]"
```

#### Option 2: Using requirements.txt (Legacy)
Alternatively, you can still use the legacy requirements files:

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r dev_requirements.txt  # for development dependencies
```

### - App dependencies
The application has a range of dependencies used in production. To make developing look as much as production as possible we use docker compose to run Redis, MinIO and PostgreSQL. If you haven't got docker go get docker desktop [here](https://docs.docker.com/desktop/)

If you have docker compose, run the following command while positioned in the root folder of the repository
```bash
docker compose up
```
This will start a range of backen applications needed.

### - 
While positioned at `/ddsc-website/ddsc_web/` (same folder as manage.py file) run the following commands.

```bash
python manage.py migrate --settings=ddsc_web.settings.dev
python manage.py collectstatic --no-input --settings=ddsc_web.settings.dev
```
This will first create the tables in your database for the website application and then collect static files and put them into the S3 bucket.

### - Starting the development server with Celery
To run the website development server, run the following command.

```bash
python manage.py runserver --settings=ddsc_web.settings.dev
```
To start the Celery task executioner run the below executable from a seperat terminal. NOTE that you will need to activate your virtual environment again in the new terminal.
```bash
./start_dev_celery.sh
```

If you want to be abble to access `/admin` you need a user with superuser status. Run the command below to create one.

```bash
python manage.py createsuperuser --settings=ddsc_web.settings.dev
```

# ddsc-website-public
