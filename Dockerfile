FROM ubuntu:17.04

RUN apt-get update
RUN apt-get install -y nginx python3 python3-pip
ADD nginx.conf /etc/nginx/
ADD upstream.conf /etc/nginx/
ADD core ./core
ADD nginx-adapter.py .
ADD requirements.txt .
RUN pip3 install -r requirements.txt

ENTRYPOINT service nginx start && python3 nginx-adapter.py