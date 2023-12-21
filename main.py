from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from datetime import datetime
from typing import List


description = """
This service was developed in accordance with the assignment of the
DevOps course during study at [HSE Master's Programme](https://www.hse.ru/en/ma/mlds/).

## Available operations

In this app you can:
1. Create a new timestamp;
2. Create a new dog;
3. Get a list of all dogs;
4. Get a dog by its pk;
5. Update a dog by its pk;
6. Get a list of dogs by selected breed.
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


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


# 2. Реализован путь /
@app.get("/")
def root():
    return "Hello! This is our clinic's microservice for storing and updating information for dogs!"


@app.post("/post", response_model=Timestamp)
def get_post(id_usr: int):
    current_time = int(datetime.now().timestamp())
    new_usr = Timestamp(id=id_usr, timestamp=current_time)
    post_db.extend([new_usr])
    return new_usr


# 4. Реализована запись собак
@app.post("/dog", response_model=Dog)
def create_dog(name: str, kind: DogType):
    new_pk = max(dogs_db.keys()) + 1
    new_dog = Dog(name=name, pk=new_pk, kind=kind)
    dogs_db[new_pk] = new_dog
    return new_dog


# 5. Реализовано получение списка собак
@app.get("/dogs_list", response_model=List[Dog])
def get_dogs_list(limit: int = 3):
    return list(dogs_db.values())[:limit]


# 6. Реализовано получение собаки по id
@app.get("/dog/{pk}", response_model=List[Dog])
def get_dog_by_pk(dog_id: int):
    if dog_id not in dogs_db:
        raise HTTPException(status_code=404, detail='This pk is not exist')
    return [val for key, val in dogs_db.items() if key == dog_id]


# 7. Реализовано получение собак по типу
@app.get("/dog/", response_model=List[Dog])
def get_dogs(dogType: DogType = None):
    if dogType is None:
        return list(dogs_db.values())

    current_dogs = []
    for _, val in dogs_db.items():
        if val.kind == dogType:
            current_dogs.append(val)
    return current_dogs


# 8. Реализовано обновление собаки по id
@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail='This pk is not exist')
    if pk != dog.pk:
        raise HTTPException(status_code=404, detail='Pk does not match index')
    dogs_db[pk] = dog
    return dog
