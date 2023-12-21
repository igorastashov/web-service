import uvicorn
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from db.models import models
from db.db import SessionLocal, engine

from db.schemas import schemas
from db.utils import utils


models.Base.metadata.create_all(bind=engine)

description = """
This service was developed in accordance with the assignment of the
DevOps course during study at [HSE Master's Programme](https://www.hse.ru/en/ma/mlds/).

## Available operations

In this app you can:
0. See basic information about the app;
1. Create a new timestamp;
2. Create a new dog;
3. Get a list of all dogs;
4. Get a dog by its pk;
5. Update a dog by its pk;
5. Get a list of dogs by breed;
6. Update a dog by its pk;.
"""

tags = [
    {
        "name": "Available operations"
    }
]

app = FastAPI(
    title="Vet Service Clinic",
    description=description,
    openapi_tags=tags,
    contact={
        'name': "Astashov I. V.",
        'url': "https://github.com/igorastashov/web-service"
    }
)


def get_user(db: Session, user_id: int):
    return db.query(models.Timestamp).filter(models.Timestamp.id == user_id).first()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=['0. Implemented path'])
def root():
    return {"msg": "Hello! This is our clinic's microservice for storing and updating information for dogs!"}


# @app.post("/post", response_model=schemas.Timestamp,
#           tags=['1. Create a new timestamp']
#           )
# def get_post(db: Session = Depends(get_db)):
#     current_time = int(datetime.now().timestamp())
#     new_usr = Timestamp(id=id_usr, timestamp=current_time)
#     post_db.extend([new_usr])
#     return new_usr


@app.post("/dog", response_model=schemas.Dog,
          tags=['2. Create a new dog']
          )
def create_dog(dog: schemas.Dog, db: Session = Depends(get_db)):
    db_dog = utils.get_dog(db=db, dog_pk=dog.pk)
    if db_dog is not None:
        raise HTTPException(status_code=409, detail="This pk is exist")
    return utils.create_dog(db=db, dog=dog)
#
#
# @app.get("/dogs_list", response_model=List[Dog],
#          tags=['3. Get a list of all dogs']
#          )
# def get_dogs_list(limit: int = 3):
#     return list(dogs_db.values())[:limit]
#
#
# @app.get("/dog/{pk}", response_model=schemas.Dog,
#          tags=['4. Get a dog by its pk']
#          )
# def get_dog_by_pk(dog_id: int, db: Session = Depends(get_db)):
#     db_dog = crud.get_dog(db=db, dog_pk=pk)
#     if dog_id not in dogs_db:
#         raise HTTPException(status_code=404, detail='This pk is not exist')
#     return [val for key, val in dogs_db.items() if key == dog_id]
#
#
# # 7. Реализовано получение собак по типу
# @app.get("/dog/", response_model=List[Dog],
#          tags=['5. Get a list of dogs by breed']
#          )
# def get_dogs(dogType: DogType = None):
#     if dogType is None:
#         return list(dogs_db.values())
#
#     current_dogs = []
#     for _, val in dogs_db.items():
#         if val.kind == dogType:
#             current_dogs.append(val)
#     return current_dogs
#
#
# @app.patch("/dog/{pk}", response_model=Dog,
#            tags=['6. Update a dog by its pk']
#            )
# def update_dog(pk: int, dog: Dog):
#     if pk not in dogs_db:
#         raise HTTPException(status_code=404, detail='This pk is not exist')
#     if pk != dog.pk:
#         raise HTTPException(status_code=404, detail='Pk does not match index')
#     dogs_db[pk] = dog
#     return dog


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
