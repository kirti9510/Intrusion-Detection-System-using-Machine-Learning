FROM python:2.7-slim
MAINTAINER Luv Singh <luv.singh@crevise.com>

ENV INSTALL_PATH /hodor
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "hodor.app:create_app()"
