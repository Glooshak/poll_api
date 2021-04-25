refresh_db:
			rm -rf polls/migrations/*
			rm -f db.sqlite3
			python manage.py makemigrations polls
			python manage.py migrate
			echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'hack_me')" | python manage.py shell

start:
			python manage.py runserver
