FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app/
COPY main.py /app/
COPY sandbox.py /app/
COPY /files/ /app/files/
COPY /tests/ /app/tests/
COPY uv.py /app/
RUN pip3 install -r requirements.txt

CMD [ "python3", "uv.py" ]