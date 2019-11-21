FROM python:3.7

COPY . /app

WORKDIR /app

pip3 install -r requirements.txt

CMD ["python3", "server.py"]