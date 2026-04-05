echo 'Installing dependencies...'
python -m pip install -r requirements.txt

echo 'Running Migrations...'
python manage.py makemigrations --noinput
python manage.py migrate --noinput