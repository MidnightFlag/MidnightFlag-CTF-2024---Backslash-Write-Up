FROM python:3.9-slim

ENV USER SageMaster

COPY ./src /app
WORKDIR /app

RUN apt-get clean && \
	apt-get update --fix-missing &&\
	apt-get -y --yes upgrade

RUN apt-get -y -qq install --yes sudo bash nano socat

EXPOSE 5000

ENTRYPOINT socat TCP-LISTEN:5000,fork,reuseaddr,bind=0.0.0.0 EXEC:"stdbuf -i0 -o0 -e0 python3 app.py"