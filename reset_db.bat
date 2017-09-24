del db.sqlite3
del dispatch\migrations\*

python manage.py makemigrations dispatch
python manage.py migrate

REM python manage.py createsuperuser --username admin@monosaur.com --email admin@monosaur.com
