FROM ubuntu:20.04
RUN apt -y update
RUN apt install python3 python3-pip git nano vim -y
RUN apt install python-is-python3 -y

WORKDIR /workspace

COPY requirements.txt .
COPY setup.py .

RUN pip install -r requirements.txt
