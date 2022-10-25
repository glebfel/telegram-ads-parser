FROM python:bullseye
MAINTAINER Gleb Felyust 'felyust@list.ru'

# copy and install all dependencies
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# copy project files
COPY . /app
WORKDIR /app

# run api
CMD ["python", "main.py"]