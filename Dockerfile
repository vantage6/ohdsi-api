FROM harbor2.vantage6.ai/infrastructure/algorithm-ohdsi-base:latest

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# port where the API is liste
EXPOSE ${PORT}

ENV LD_LIBRARY_PATH=/usr/lib/jvm/java-17-openjdk-amd64/lib/server/

RUN pip install psycopg2-binary
# start the flask app
# CMD uwsgi --http 0.0.0.0:${PORT} --master -p 4 -w run:app
CMD gunicorn -b 0.0.0.0 -w 1 'api:app'

# /usr/local/lib/python3.11/site-packages/ohdsi/database_connector