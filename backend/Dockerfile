FROM python:3.11-bullseye

WORKDIR /api-docker

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . /api-docker/

CMD ["python3", "src/app.py"]