from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime
from bson.objectid import ObjectId

class Availability(BaseModel):
    start_time: datetime
    end_time: datetime

class Therapist(BaseModel):
    name: str
    username: str
    password: str
    email: str
    description: str
    specialization: List[str]
    availability: List[Availability]
    ratings: List[str]
    available: bool = True


class LoginModel(BaseModel):
    username: str
    password: str