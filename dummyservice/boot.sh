#!/bin/sh -e

FLASK_APP=app.py

#FOR DATABASE init
#flask db init
#For DATABASE migration
#flask db migrate -m "update"

# sync database to latest migration
flask db upgrade
exec gunicorn --log-level info --log-file=/gunicorn.log --workers 4 --name app -b 0.0.0.0:8000 --reload app:app
