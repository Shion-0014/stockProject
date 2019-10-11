FROM python:3.6

WORKdIR /usr/workdir

COPY . /usr/workdir
RUN pip install --no-cache-dir -r requirements.txt
