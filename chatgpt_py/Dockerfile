FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y chromium-bsu chromium-driver 
RUN apt-get install python3 python3-pip -y

RUN pip3 install flask
COPY requirements.txt /
RUN pip3 install -r requirements.txt

RUN mkdir /app