from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import fake_users_db, UserInDB

app = FastAPI()

# Models
class User(BaseModel):
    name: str
    age: int
    email: str

# Get all users
@app.get("/users", response_model=List[User])
def get_users():
    return list(fake_users_db.values())

# Get a single user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = fake_users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new user
@app.post("/users", response_model=User)
def create_user(user: User):
    user_id = max(fake_users_db.keys()) + 1 if fake_users_db else 1
    new_user = UserInDB(id=user_id, **user.dict())
    fake_users_db[user_id] = new_user
    return new_user

# Update a user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    fake_users_db[user_id].name = updated_user.name
    fake_users_db[user_id].age = updated_user.age
    fake_users_db[user_id].email = updated_user.email
    return fake_users_db[user_id]

# Delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_users_db[user_id]
    return {"detail": "User deleted successfully"}
