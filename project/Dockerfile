FROM python:3.6

# set work directory
WORKDIR /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /project/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /project
