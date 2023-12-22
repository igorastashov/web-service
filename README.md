## FastAPI Web Service - Vet Clinic

**FastAPI web service for a vet clinic to store and update the information about dogs.**

Astashov I.V., 2023.

This service was developed in accordance with the assignment of the
DevOps course during study at [HSE Master's Programme](https://www.hse.ru/en/ma/mlds/).

**If you would like to use the deployed service on Render see [(3) Quick start](https://github.com/igorastashov/web-service/blob/dev/README.md#3-quick-start).**


## (1) Task

The clinic needs a microservice to store and update information for dogs 
in accordance with the [documentation](https://github.com/igorastashov/web-service/blob/dev/clinic.yaml) in OpenAPI format.


## (2) Technologies

- Python 3.11
- Fast API
- Postgres
- SQLAlchemy
- Uvicorn


## (3) Quick start

The service is deployed on Render. See the documentation at the [link](https://fastapi-vet-service-with-db-postgres.onrender.com/docs).


## (4) Local Development

1. Clone this repo and `cd` into repo directory
2. Create a virtual environment: `python -m venv venv`
3. Activate a virtual environment: `source venv/Scripts/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn main:app --reload`
6. Access swagger at: http://127.0.0.1:8000/docs


## (5) Schema

Dog
- name
- kind
- pk

Timestamp
- id
- timestamp


## (6) Design API

**/**

- GET: Basic information about the app

**/post**

- POST: Create a new id and timestamp

**/dog**

- POST: Create a new dog

**/dog**

- GET: Get a list of all dogs or list of dogs by type

**/dog/{pk}**

- GET: Get a dog by pk

**/dog/{pk}**

- PATCH: Update a dog by pk


## (A) Acknowledgments

This repository borrows partially from [Артём Шумейко](https://www.youtube.com/watch?v=_1H1qsNqxwM&list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS&index=16) and [Gwendolyn Faraday](https://github.com/gwenf/python-polls).
