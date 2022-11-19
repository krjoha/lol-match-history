FROM ubuntu:20.04
RUN apt -y update
RUN apt install python3 python3-pip python3-dev build-essential git nano vim -y
RUN apt install python-is-python3 -y
RUN pip3 install --upgrade pip

WORKDIR /workspace

COPY requirements.txt .
COPY setup.py .

RUN pip install -r requirements.txt
