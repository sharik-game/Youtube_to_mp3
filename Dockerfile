# Dockerfile

# pull the official docker image
FROM python:3.10-slim

# set work directory
# WORKDIR .

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .