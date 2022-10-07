## Run in development mode

1. Clone the repo
2. Run `docker compose -f docker-compose.dev.yml up --build`

## Run in Production mode

Copy directory named `data` in the project root to the server

Copy the file named `init-letsencrypt.sh` to the server

Copy `docker-compose.prod.yml`

Run `init-letsencrypt.sh`

Run `docker compose -f docker-compose.prod.yml -f up -d`

### References

    https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
    https://github.com/wmnnd/nginx-certbot
