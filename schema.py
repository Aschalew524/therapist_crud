from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime
from bson import ObjectId

class AvailabilitySchema(BaseModel):
    start_time: datetime
    end_time: datetime

class TherapistSchema(BaseModel):
    name: str
    username: str
    password: str                                                                                                      
    email: str
    description: str
    specialization: List[str]
    availability: List[AvailabilitySchema]
    ratings: List[str]
    available: bool = True

class UserSchema(BaseModel):
    username: str
    password: str
