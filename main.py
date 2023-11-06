from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime
from typing import List

app = FastAPI(
    title="Vet Service Clinic"
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


# 3. Реализован путь /post
@app.post("/post", response_model=List[Timestamp])
def get_post():
    id_max = 0
    for i in post_db:
        if i.id > id_max:
            id_max = i.id

    new_id = id_max + 1
    current_time = int(datetime.now().timestamp())
    new_usr = Timestamp(id=new_id, timestamp=current_time)
    post_db.extend([new_usr])
    return [new_usr]


# 4. Реализована запись собак
@app.post("/dog", response_model=List[Dog])
def create_dog(name: str, kind: DogType):
    new_pk = max(dogs_db.keys()) + 1
    new_dog = Dog(name=name, pk=new_pk, kind=kind)
    dogs_db[new_pk] = new_dog
    return [new_dog]


# 5. Реализовано получение списка собак
@app.get("/dogs_list")
def get_dogs_list(limit: int = 1):
    return list(dogs_db.values())[:limit]


# 6. Реализовано получение собаки по id
@app.get("/dog/{pk}", response_model=List[Dog])
def get_dog_by_pk(dog_id: int):
    return [val for key, val in dogs_db.items() if key == dog_id]


# 7. Реализовано получение собак по типу
@app.get("/dog/")
def get_dogs(dogType: DogType):
    current_dogs = []

    for key, val in dogs_db.items():
        if val.kind == dogType:
            current_dogs.append(val)
    return current_dogs


# 8. Реализовано обновление собаки по id
@app.patch("/dog/{pk}", response_model=List[Dog])
def update_dog(pk: int, new_name: str):
    current_dog = []
    for key, val in dogs_db.items():
        if val.pk == pk:
            val.name = new_name
            current_dog.append(val)
    return current_dog
