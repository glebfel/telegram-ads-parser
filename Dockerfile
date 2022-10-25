FROM python:bullseye
MAINTAINER Gleb Felyust 'felyust@list.ru'

# copy and install all dependencies
COPY app/requirements.txt /app/
RUN pip install -r /app/requirements.txt

# copy project files
COPY ./app /app
WORKDIR /app

# run api
CMD ["python", "main.py"]