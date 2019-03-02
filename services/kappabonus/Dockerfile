FROM ubuntu:18.04

EXPOSE 3377

WORKDIR /app/
COPY requirements.txt /requirements.txt
RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install --no-cache -r /requirements.txt
COPY . /app/

RUN ["python3", "app.py"]

