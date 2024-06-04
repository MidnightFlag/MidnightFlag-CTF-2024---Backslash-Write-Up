FROM ubuntu:20.04

COPY ./src /app
WORKDIR /app

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd
RUN chown -R root:root /app

RUN apt-get update && apt-get -y install socat

USER ctf

EXPOSE 1234
ENTRYPOINT socat TCP-LISTEN:1234,fork,reuseaddr,bind=0.0.0.0 EXEC:"./letmebuy",pty,raw,echo=0