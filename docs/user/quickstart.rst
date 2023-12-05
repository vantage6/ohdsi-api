Quickstart
==========

Basic Usage
------------
Make sure you have the following:

* An running OMOP data source
* Docker installed

Make sure you have Docker installed. Create a new directory and copy the following
contents into a file called ``docker-compose.yml``:

.. code-block:: yaml
    :caption: docker-compose.yml

    services:

        # OHDSI API
        ohdsi-api:
            image: harbor2.vantage6.ai/infrastructure/ohdsi-api:latest
            ports:
            - 5000:8000
            volumes:
            - .:/app
            container_name: ohdsi-api
            env_file:
            - .connection-details.env
            command: ["gunicorn", "-b", "0.0.0.0", "-w", "1", "api:app"]

        # RabbitMQ
        rabbitmq:
            image: rabbitmq:3-management
            ports:
            - 5672:5672
            - 15672:15672
            container_name: rabbitmq

        # PostgreSQL for celery
        db:
            image: postgres:9.6
            ports:
            - 5454:5432
            container_name: postgres
            environment:
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=Celery@Postgr3s!
            - POSTGRES_DB=celery
            volumes:
            - ./data/postgres:/var/lib/postgresql/data

        celery-worker:
            image: harbor2.vantage6.ai/infrastructure/ohdsi-api:latest
            container_name: celery-worker
            command: celery -A api.celery_app worker -l DEBUG -P solo
            env_file:
            - .connection-details.env
            volumes:
            - .:/app
            depends_on:
            - rabbitmq

Then you need to create a ``.connection-details.env`` file with the connection details to the
OMOP data source:

.. code-block:: sh
    :caption: .connection-details.env

    CELERY_BROKER_URL=amqp://[USERNAME]:[USERNAME]@rabbitmq:5672/
    CELERY_RESULT_BACKEND=db+postgresql://[USERNAME]:[PASSWORD]@[HOST]/[DATABASE]

    OMOP_DBMS=postgresql
    OMOP_HOST=omop-data-source
    OMOP_PORT=5432
    OMOP_USER=ohdsi
    OMOP_PASSWORD=ohdsi
    OMOP_DB=ohdsi
    OMOP_CDM_SCHEMA=cdm

Finally, start the API by running:

.. code:: bash

    docker compose up -d

This will start the API on port 5000. You can now access the API on
``http://localhost:5000``. To see all available endpoints, visit
``http://localhost:5000/apidocs``.

