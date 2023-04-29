create_super_user:
	python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('alumnodb', 'alumnodb@uam.es', 'alumnodb')"

populate:
	python3 ./manage.py populate

runserver: 
	python3 manage.py runserver 8003

update_models:
	python3 manage.py makemigrations
	python3 manage.py migrate

dbshell:
	./manage.py dbshell

shell:
	./manage.py shell

clean:
	rm -rf __pycache__