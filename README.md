# Clone the repo

git clone git@github.com:Atomnp/certification-system-backend.git
cd certification-system-backend

# Create a virtual environment to isolate our package dependencies locally

python3 -m venv env
source env/bin/activate # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtual environment

pip install django
pip install djangorestframework

# Run

With vscode:

1. Press f5

Without vscode:

1. Goto directory containing manage.py
2. python manage.py runserver

Run in development mode

`docker compose -f docker-compose.dev.yml up --build`

## Run in Production mode

Copy directory named `data` in the project root to the server
Copy the file named `init-letsencrypt.sh` to the server
Copy `docker-compose.prod.yml`

Run `init-letsencrypt.sh`
Run `docker compose -f docker-compose.prod.yml -f up -d`

### References

    https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
    https://github.com/wmnnd/nginx-certbot
