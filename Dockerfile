FROM python:3.9.7-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
# COPY ./myproject /app
RUN mkdir /app
COPY . /app/

WORKDIR /app/certification_system

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
