FROM python:3.9-slim

WORKDIR /app

COPY etl.py /app/

RUN pip install boto3 PSYCOPG-BINARY python-dotenv 


CMD [ "python","etl.py" ]