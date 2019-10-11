FROM python:3.6

WORKDIR /usr/work

COPY ./requirements.txt /usr/work
RUN pip install --no-cache-dir -r requirements.txt
