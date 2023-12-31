FROM python:3.10.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
#RUN apt-get update && apt-get install -y gettext 
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/