# Test

### Install python3

	sudo apt install python3

### Install virtual environment

	sudo apt-get install python3-venv

### Create virtual environment

	python3 -m venv test

### Activate virtual environment

	source test/bin/activate

### Install Requirements

	python -m pip install --upgrade pip
	pip install -r requirements.txt

### Migrate

	python manage.py migrate

### Create Admin Account (Optional)

	python manage.py createsuperuser

### Runserver

	python manage.py runserver

### Run in localhost

	Open localhost:8000 in your browser
