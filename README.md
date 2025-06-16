# Superheroes API

A simple Flask-based REST API to manage heroes, powers, and hero-powers relationships.

## Author
Cyprian Kanda

## Features
- Get all heroes and specific hero details with powers
- Get and update powers
- Assign powers to heroes

## Setup Instructions
```bash
git clone https://github.com/cypriankanda/superhero_api.git
cd superhero_api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
python seed.py
flask run
