FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN mkdir /app 
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN python3 -m pip install tensorflow
RUN python3 -m pip install keras
# RUN pip3 install flask
RUN export FLASK_APP=app.py
RUN export FLASK_ENV=development
# RUN flask run
# ENTRYPOINT ["python3"]
CMD ["flask","run"]