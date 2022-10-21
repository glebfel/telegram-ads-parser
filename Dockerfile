FROM python:bullseye
MAINTAINER Gleb Felyust 'felyust@list.ru'

# copy project files and all dependencies
COPY ./app /app
WORKDIR /app

# install all dependencies
RUN pip install -r requirements.txt

CMD ["python3","main.py"]