FROM python:3.8.5

WORKDIR /app

ADD . /app
RUN pythom -m pip install --upgrade pip
RUN pip3 install Flask==1.1.2 flask-restx==0.2.0 pymysql==1.0.2 requests==2.25.1
RUN pip3 install uwsgi


CMD ["uwsgi","uwsgi.ini"]