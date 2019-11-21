FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "api/server.py"]