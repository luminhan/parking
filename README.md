# Django API Project - Parking


* [Django Admin](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/) configured and also with the Label A skinning package to build backoffice integrations.
* [REST Framework](https://www.django-rest-framework.org/) - API endpoint development framework built on top of Django. Minimally configured so you can do whatever you want with your project.
* [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) - generates Swagger documentation for your REST Framework endpoints at `/swagger`.

This is all wrapped up into a docker-compose environment with development defaults. Postgres, Redis server are all preconfigured.


### Django
* Application with the name `project` created
* `apps/` module created for our apps
* Cache enabled with Redis backend

### `shared` App
* Tests for health check endpoint
* Test factories implemented for User and Group models

### `authentication` App
* Custom user model that uses email instead of username as primary

### REST Framework
* Integrated into Django
* Standard base config defined in `settings.py`
* Swagger documentation generation configured at `/swagger`, `/swagger.json`, `/swagger.yaml`

## Usage

### Setup

* Run `docker-compose build`
* Run migrations with `docker-compose run --rm backend ./manage.py migrate`
* Create a superuser with `docker-compose run --rm backend ./manage.py createsuperuser`

### Running

`docker-compose up` to start the project

* [http://localhost:8000/api](http://localhost:8000/api) to access the API
* [http://localhost:8000/swagger](http://localhost:8000/swagger) to access the swagger
* [http://localhost:8000/admin](http://localhost:8000/admin) to access the admin

### Operations

These operations assume the project is already up and are to be run in a second terminal session.

* **Flake8**: `docker-compose exec backend flake8`
* **Run tests**: `docker-compose exec backend ./manage.py test`
* **Run specific tests**: `docker-compose exec backend ./manage.py test apps/cookiecutter`
* **Run tests with coverage**: `docker-compose exec backend sh -c "coverage run --source='.' ./manage.py test  && coverage report -m --omit=fabfile.py,*/tests/*,*/migrations/*"`
* **Generate migrations**: `docker-compose exec backend ./manage.py makemigrations`
* **Run migrations**: `docker-compose exec backend ./manage.py migrate`
* **Create superuser**: `docker-compose exec backend ./manage.py createsuperuser`
* **Create a new app**: `docker-compose exec backend ./manage.py startapp <APP_NAME>` (and drag it into the `apps/` folder)
* **Run the project in the background**: `docker-compose up -d`

### Teardown

* **Completely stop the project**: `docker-compose down`
* **Delete the project and delete database data**: `docker-compose down -v`

