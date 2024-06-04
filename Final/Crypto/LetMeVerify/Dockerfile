FROM sagemath/sagemath

ENV USER SageMaster

COPY ./src /app
WORKDIR /app

RUN sudo apt-get clean && \
	sudo apt-get update --fix-missing &&\
	sudo apt-get -y --yes upgrade

RUN sudo apt-get -y -qq install --yes sudo bash nano socat netcat wget iproute2 curl 

RUN sudo chown -R "sage":"sage" /app
EXPOSE 5000

ENTRYPOINT socat TCP-LISTEN:5000,fork,reuseaddr,bind=0.0.0.0 EXEC:"stdbuf -i0 -o0 -e0 /home/sage/sage/local/var/lib/sage/venv-python3.11.1/bin/python3 app.py"
