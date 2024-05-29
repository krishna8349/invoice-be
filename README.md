# invoice-be
This is a backend repo for invoice
This project is the invoice Services server. It primarily is a REST API interface, is also manages a database. It is built using Django and PostgreSQL.

This README is targeted to developers to assist setting up this project and committing code.


## Initial Local Setup

This project is set up using the standards of Django Rest framework. The following resources will help guide you through setup:
- [Django](https://docs.djangoproject.com/en/3.2/) documentation
- [Django REST Framework](https://www.django-rest-framework.org/) documentation

### Prerequisites
Download and install the following:

- Python 3.8.x
- [Virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for Python
- [Postgres](https://www.postgresql.org/download/)
    - If you are on a Mac, [Postgres.app](https://postgresapp.com/) is a very convienient installation of Postgres
- You are free to use any IDE that works for you. Visual Studio Code works well for the team.

### Clone the repository
```
git clone git@github.com:app-sphere-softwares-llp/invoice-be.git
```

### Install packages
Packages are managed with Pip.
```
pip install -r requirements.txt
```
If you get errors while installing packages and have Python installed previously, you can manually check / install packages that are outdated:
```
pip list --outdated
```

### Create a database
In your database IDE or via command line, create a new empty database. Note your database name, host, user, and password.
```
CREATE DATABASE db_name;
```

### Local Configuration
Create a copy of `invoice-be/apps/local_settings.example.py` and name it `local_settings.py`.

Set your local variables for your new database and Redis instance here.

There are many other environment variables being used for connecting to external resources. Request these from the lead developer.

### Migrate Schemas

run the migration scripts:
```
python manage.py migrate
```


### Start up the server
```
python manage.py runserver
```

### Log in
You're good to go! Navigate to your tenant url in our browser (for example: `http://127.0.0.1:8000/admin/`).

## Checking in new code
To get you productive and checking in new code, here a few standard practices to follow:

### Unit Tests
Make sure to add unit tests to your stories. We are using `pytest` and `unittest`. Unit tests are expected for both functional components, as well as REST endpoints.

Unit tests will be run on a pre-commit hook, so all tests will need to pass before you can commit code.

To run the tests:
```
pytest --cov=invoice-be/
```
