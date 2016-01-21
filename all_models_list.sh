#!/bin/bash

python manage.py list_all_models 2> "list_on_`date +"%Y-%m-%d"`.dat" 1> /dev/null
