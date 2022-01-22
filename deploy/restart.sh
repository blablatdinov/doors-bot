cd /home/www/code/doors-bot

git pull
git reset --hard origin/test

/home/www/.poetry/bin/poetry install
/home/www/.poetry/bin/poetry run python manage.py migrate

sudo supervisorctl restart doors-bot
