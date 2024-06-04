FROM sagemath/sagemath

ENV USER SageMaster

COPY ./src /app
WORKDIR /app

RUN sudo apt-get clean && \
	sudo apt-get update --fix-missing &&\
	sudo apt-get -y --yes upgrade

RUN sudo apt-get -y -qq install --yes sudo bash nano socat netcat wget iproute2 curl 

RUN /home/sage/sage/local/var/lib/sage/venv-python3.11.1/bin/python3 -m pip install --upgrade pip && \
	/home/sage/sage/local/var/lib/sage/venv-python3.11.1/bin/python3 -m pip install -r /app/requirements.txt

RUN sudo chown -R "sage":"sage" /app
EXPOSE 5000

CMD ["/app/start.sh"]