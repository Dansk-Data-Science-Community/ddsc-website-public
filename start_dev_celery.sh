#!/bin/bash

export DJANGO_SETTINGS_MODULE=ddsc_web.settings.dev
cd ddsc_web
celery --app=ddsc_web worker -l INFO