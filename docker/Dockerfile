FROM        ubuntu:20.04

COPY	    requirements.txt .

RUN         apt-get update \
         && apt-get install -y python3 python3-pip python3-dev build-essential


RUN	        pip3 install --upgrade -r requirements.txt

RUN         mkdir /app

COPY        src/ /app

WORKDIR     /app

RUN         pip3 install tensorflow==2.3.2
RUN         pip3 install keras.models

ENTRYPOINT  ["python3"]
CMD         ["app.py"]