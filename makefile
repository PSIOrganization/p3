create_super_user:
	python3 ./manage.py createsuperuser

populate:
	python3 ./manage.py populate

runserver: 
	python3 manage.py runserver 8001

update_models:
	python3 manage.py makemigrations
	python3 manage.py migrate

dbshell:
	./manage.py dbshell

shell:
	./manage.py shell

clean:
	rm -rf __pycache__