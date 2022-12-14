import uuid

from fastapi import FastAPI, HTTPException
from models import User, Role
from typing import List
from uuid import UUID, uuid4
from fastapi.encoders import jsonable_encoder

import json

app = FastAPI()

db: List[User] = []


def load_db():
    with open('user_db.json', 'r') as file:
        data = json.load(file)

        for person in data:
            user = User(
                id=uuid.UUID(person['id']),
                first_name=person['first_name'],
                last_name=person['last_name'],
                email=person['email'],
                roles=[Role.user]
            )
            db.append(user)


def save_db():
    json_user_db = json.dumps(jsonable_encoder(db), indent=4)
    with open('user_db.json', 'w') as db_file:
        db_file.write(json_user_db)


# def fetch_users():
#     file = open('MOCK_USER_DATA.json')
#     data = json.load(file)
#
#     for person in data:
#         user = User(
#             id=uuid4(),
#             first_name=person['first_name'],
#             last_name=person['last_name'],
#             email=person['email'],
#             roles=[Role.user]
#         )
#         db.append(user)
#
#
# fetch_users()
#
# json_user_db = json.dumps(jsonable_encoder(db), indent=4)
# with open("user_db.json", "w") as file:
#     file.write(json_user_db)

load_db()


# Path operations are evaluated in order!!!
@app.get("/")
async def root():
    return db


@app.get("/users")
async def get_users():
    return db


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    converted_id = uuid.UUID(user_id)

    for db_user in db:
        if converted_id == db_user.id:
            return db_user
        else:
            raise HTTPException(status_code=404, detail="User not found")


@app.post("/users")
async def create_user(user: User):
    if user in db:
        return user
    else:
        db.append(user)


@app.put("/users/{user_id}")
async def update_user(user_id: str, updated_user: User):
    for db_user in db:
        converted_id = uuid.UUID(user_id)
        if converted_id == db_user.id:
            db.pop(db.index(db_user))
            db.append(updated_user)
            return updated_user
        else:
            raise HTTPException(status_code=404, detail="User not found")


@app.delete("users/{user_id}")
async def delete_user(user_id: str):
    for db_user in db:
        converted_id = uuid.UUID(user_id)
        if converted_id == db_user.id:
            db.pop(db.index(db_user))
        else:
            raise HTTPException(status_code=404, detail="User not found")
