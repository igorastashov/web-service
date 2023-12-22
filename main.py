from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db.db import SessionLocal
from db.schemas import schemas
from db.sessions import sessions

description = """
This service was developed in accordance with the assignment of the
DevOps course during study at [HSE Master's Programme](https://www.hse.ru/en/ma/mlds/).

## Available operations

In this app you can:
1. See basic information about the app;
2. Create a new timestamp;
3. Create a new dog;
4. Get a list of all dogs or list of dogs by type;
5. Get a dog by its pk;
6. Update a dog by its pk;
"""

tags = [{"name": "Available operations"}]

app = FastAPI(
    title="Vet Service Clinic",
    description=description,
    openapi_tags=tags,
    contact={
        "name": "Astashov I. V.",
        "url": "https://github.com/igorastashov/web-service",
    },
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["1. See basic information about the app"])
def root():
    return {
        "msg": "Hello! This is our clinic's microservice for storing and updating information for dogs!"
    }


@app.post("/post", response_model=schemas.Timestamp, tags=["2. Create a new timestamp"])
def get_post(timestamp: schemas.Timestamp, db: Session = Depends(get_db)):
    db_timestamp = sessions.get_timestamp(db=db, timestamp_id=timestamp.id)
    if db_timestamp is not None:
        raise HTTPException(
            status_code=409, detail="Timestamp with this id already exists"
        )
    return sessions.create_timestamp(db=db, timestamp=timestamp)


@app.post("/dog", response_model=schemas.Dog, tags=["3. Create a new dog"])
def create_dog(dog: schemas.Dog, db: Session = Depends(get_db)):
    db_dog = sessions.get_dog(db=db, dog_pk=dog.pk)
    if db_dog is not None:
        raise HTTPException(status_code=409, detail="This pk is exist")
    return sessions.create_dog(db=db, dog=dog)


@app.get(
    "/dog",
    response_model=list[schemas.Dog],
    tags=["4. Get a list of all dogs or list of dogs by type"],
)
def get_dogs(kind: schemas.DogType = None, db: Session = Depends(get_db)):
    dogs = sessions.get_dogs(db=db, kind=kind)
    return dogs


@app.get("/dog/{pk}", response_model=schemas.Dog, tags=["5. Get a dog by its pk"])
def get_dog_by_pk(pk: int, db: Session = Depends(get_db)):
    db_dog = sessions.get_dog(db=db, dog_pk=pk)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return db_dog


@app.patch("/dog/{pk}", response_model=schemas.Dog, tags=["6. Update a dog by its pk"])
def update_dog(pk: int, dog: schemas.Dog, db: Session = Depends(get_db)):
    db_dog = sessions.get_dog(db=db, dog_pk=pk)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="This pk is not exist")
    db_dog = sessions.get_dog(db=db, dog_pk=dog.pk)
    if pk != dog.pk and db_dog is not None:
        raise HTTPException(status_code=409, detail="Pk does not match index")
    return sessions.update_dog(db=db, dog=dog)
