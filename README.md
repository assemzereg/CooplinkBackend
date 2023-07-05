***This is a backend that contains an ai model that predicts the suitable production chain for your products according to the budget and optimizes quality***      

***it has a PostgreSQL database with a docker container to run it locally and APIs with all the CRUD System***






To start the server:

Create venv with python -m venv venv

Install requirements pip install -r requirements.txt

Start docker compose docker-compose up -d

Run run.py with PyCharm.
Execute migrations flask db upgrade

Visit localhost:5433

Create a user and go to localhost:5000/users
