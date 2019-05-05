del db.sqlite3
del monzodispatch\migrations\*

python manage.py makemigrations monzodispatch
python manage.py migrate

REM python manage.py createsuperuser --username admin@monosaur.com --email admin@monosaur.com
