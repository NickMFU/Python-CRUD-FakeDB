from typing import Dict
from pydantic import BaseModel

class UserInDB(BaseModel):
    id: int
    name: str
    age: int
    email: str

# In-memory fake database
fake_users_db: Dict[int, UserInDB] = {}
