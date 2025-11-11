#!/bin/bash

cp celery.service /etc/systemd/system/celery.service
cp celeryd /etc/default/celeryd
systemctl daemon-reload
systemctl enable celery
systemctl restart celery