FROM python:3.6-alpine

RUN apk update
RUN apk add ttf-freefont chromium chromium-chromedriver
RUN apk --update-cache add python3-dev postgresql-client \
    gcc g++ libc-dev linux-headers postgresql-dev
RUN apk  add freetype-dev

RUN mkdir /noto
ADD https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip /noto
WORKDIR /noto
RUN unzip NotoSansCJKjp-hinted.zip && \
    mkdir -p /usr/share/fonts/noto && \
    cp *.otf /usr/share/fonts/noto && \
    chmod 644 -R /usr/share/fonts/noto/ && \
    fc-cache -fv
RUN rm -rf /noto

WORKDIR /usr/work

COPY ./requirements.txt /usr/work
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

