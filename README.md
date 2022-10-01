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
