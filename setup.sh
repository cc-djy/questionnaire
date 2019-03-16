#!/bin/sh

gunicorn -w4 -b 0.0.0.0:8000 questionnaire.wsgi
