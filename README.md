# shop-cosmetics

Descripton

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them
* install virtualenv

### Installing

* First install virtualenv if it is not preinstalled
```
pip install virtualenv
```
* Activate Virtual environment in the project directory

```
source venv/bin/activate
```

* Migrate the database
```
python manage.py makemigrations
python manage.py migrate
```
* run django

```
python manage.py runserver
```
## Endponints

* To see url endpints go to 'test2/urls.py' and 'core/urls.py'
## Admin page
* First create a superuser
```
python manage.py createsuperuser
```
* Then login using your creaditnails you were provided
* go to 127.0.0.1:8000/admin/ to login and manage your db

# TODO

* Fix 'Favorites'

# Endpoints
* [Endpoint guidlines for this project](docs/guidlines.md)
