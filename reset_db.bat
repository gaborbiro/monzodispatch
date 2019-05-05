REM Unix/Linux only!

REM delete database and migration files
del db.sqlite3
del     monzodispatch\migrations\*

REM regenerate migration files and database based on current models
python manage.py makemigrations monzodispatch
python manage.py migrate

python manage.py createsuperuser --username admin@canibuyit.com --email admin@canibuyit.com
