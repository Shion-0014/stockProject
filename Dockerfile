FROM python:3.6

WORKdIR /usr/work

COPY ./requirements.txt /usr/work
RUN pip install --no-cache-dir -r requirements.txt
