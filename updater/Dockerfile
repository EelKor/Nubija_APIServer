FROM python:3.8.5

WORKDIR /main

ADD . /main
RUN pythom -m pip install --upgrade pip
RUN pip3 install pymysql==1.0.2 requests==2.25.1

CMD ["python","main.py"]