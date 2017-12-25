#!/bin/sh


sleep 5
cd translation_caching
su -m myuser -c "celery worker -A translation_caching.celery -Q default -n default@%h"
