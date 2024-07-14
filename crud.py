from typing import List, Optional
from bson.objectid import ObjectId
from models import Therapist
from schema import TherapistSchema

def create_therapist(db, therapist: Therapist):
    result = db.therapist.insert_one(therapist.dict())
    return result.inserted_id

def get_therapist(db, therapist_id: str):
    therapist = db.therapist.find_one({"_id": ObjectId(therapist_id)})
    if therapist:
        return TherapistSchema(**therapist)
    return None

def get_all_therapists(db) -> List[Therapist]:
    therapists = db.therapist.find()
    return [TherapistSchema(**t) for t in therapists]

def update_therapist(db, therapist_id: str, update_data: dict):
    result = db.therapist.update_one({"_id": ObjectId(therapist_id)}, {"$set": update_data})
    return result.modified_count

def delete_therapist(db, therapist_id: str):
    result = db.therapist.delete_one({"_id": ObjectId(therapist_id)})
    return result.deleted_count