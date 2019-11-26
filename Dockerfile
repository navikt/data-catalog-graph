FROM python:3.8

COPY . /app
COPY ca-bundle.crt /etc/ssl/certs/ca-bundle.crt
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "api/server.py"]