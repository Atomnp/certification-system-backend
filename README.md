## CERTIFICATION SYSTEM BACKEND
This repository contains system for bulk certificate generation and the system to manage certificates for online  verification.

## Run in development mode

1. Clone the repo
2. Run `docker compose -f docker-compose.dev.yml up --build`

NOTE: on windows you need to change the line ending from CRLF to LF this can be done in vscode by selecting from the bottom right side.

About CRLF: https://stackoverflow.com/a/1552775/11594030

## Run in Production mode

Copy directory named `data` in the project root to the server

Copy the file named `init-letsencrypt.sh` to the server

Copy `docker-compose.prod.yml`

Run `init-letsencrypt.sh`

Run `docker compose -f docker-compose.prod.yml up -d`

### References

    https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
    https://github.com/wmnnd/nginx-certbot

## Issues

1. If the deployed version of the app have an error that event.event is not a table, manually get inside the docker container and run makemigrations for each app
