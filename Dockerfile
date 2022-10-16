FROM python:3.8-slim-buster

RUN pip install --upgrade pip

COPY ./requirements.txt .

# This installs dependencies needed for opencv
RUN apt-get update -y && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
# COPY ./myproject /app
RUN mkdir /app
COPY . /app/

WORKDIR /app/certification_system

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
