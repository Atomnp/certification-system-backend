FROM python:3.9.7-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
# COPY ./myproject /app
RUN mkdir /app
COPY ./certification_system/ /app/

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]