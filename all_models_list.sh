#!/bin/bash

cd django_hello_world
python manage.py list_all_models 2 > "../list_on_`date +"%Y-%m-%d"`.dat"