# dj-notes

Commands to deploy to heroku

1. heroku container:push web -a=<heroku_app_name>
2. heroku container:release web -a <heroku_app_name> web
3. heroku run python manage.py makemigrations -a <heroku_app_name>
3. heroku run python manage.py migrate -a <heroku_app_name>
