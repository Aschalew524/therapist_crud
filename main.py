from fastapi import FastAPI, HTTPException, status
from crud import create_therapist, get_therapist, get_all_therapists, update_therapist, delete_therapist
from models import Therapist
from schema import TherapistSchema
from connection import db
from typing import List, Optional

app = FastAPI()

@app.post("/therapists", status_code=status.HTTP_201_CREATED)
def create_new_therapist(therapist: Therapist):
    try:
        # Check if email already exists
        existing_therapist = db.therapist.find_one({"email": therapist.email})
        if existing_therapist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Therapist with this email already exists")

        # Insert the new therapist
        result = db.therapist.insert_one(therapist.dict())
        inserted_therapist = db.therapist.find_one({"_id": result.inserted_id})
        inserted_email = str(inserted_therapist['email'])
        return {"message": f"Therapist with email {inserted_email} has been created."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# @app.get("/therapists/{therapist_id}", response_model=TherapistSchema)
# def get_therapist_by_id(therapist_id: str):
#     therapist = get_therapist(db, therapist_id)
#     if not therapist:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Therapist not found")
#     return 
@app.get("/therapists/{therapist_id}", response_model=TherapistSchema)
def get_therapist_by_id(therapist_id: str):
    try:
        therapist = get_therapist(db, therapist_id)
        return therapist
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Therapist not found: {e}")

@app.get("/therapists", response_model=List[TherapistSchema])

def list_all_therapists():
    therapists = db.therapist.find()
    return [TherapistSchema(**t) for t in therapists]


@app.patch("/therapists/{therapist_id}", response_model=TherapistSchema)
def update_therapist_info(therapist_id: str, update_data: TherapistSchema):
    # Retrieve current data
    current_data = get_therapist(db, therapist_id)
    if not current_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Therapist not found")
    
    # Update fields with provided data
    update_dict = update_data.dict(exclude_unset=True)
    updated_data = current_data.copy(update=update_dict)
    
    # Update the database entry
    modified_count = update_therapist(db, therapist_id, updated_data.dict())
    if modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Therapist not found")
    
    # Retrieve the updated data
    updated_therapist = get_therapist(db, therapist_id)
    return updated_therapist


@app.delete("/therapists/{therapist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_therapist_by_id(therapist_id: str):
    deleted_count = delete_therapist(db, therapist_id)
    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Therapist not found")
    return {"Therapist successfully deleted"}

