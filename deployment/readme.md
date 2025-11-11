# Deployment instructions
These are the instructions to deploy a new version of the DDSC website.  

**Remember to run all the Django commands with '--settings=ddsc_web.settings.staging'**

- `sudo su django`
- `cd ~django/ddsc_website`
- `git pull`
- `git branch` *check that we actually are on the 'staging' branch!*
- `source env/bin/activate`
- `python -m pip install -r requirements.txt` *an error about 'python not found' probably means the virtual environment isn't activated*
- `cd ddsc_web`
- `python manage.py migrate --settings=ddsc_web.settings.staging`
- `python manage.py collectstatic --settings=ddsc_web.settings.staging`
- `systemctl restart gunicorn`
- `systemctl restart celery`

## Troubleshooting
Troubleshooting Django logs via `journalctl -e -u gunicorn.service`