from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

class Patient(BaseModel):
    patient_id: str
    symptom: str
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()
patient_db ={
    'jack': {"patient_id": 'jack', "symptom": "fever"},
    'jill': {"patient_id": 'jill', "symptom": "scratch"},
    'jane': {"patient_id": 'jane', "symptom": "vomiting"}
    }
@app.get("/patients")
def get_patients():
    patient_list= list(patient_db.values())
    return patient_list

@app.get("/patients/{patient_id}")
async def get_(patient_id: str):
    return patient_db[patient_id]

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.post('/patients')
def create_patient(patient: Patient):
    patient_id= patient.patient_id
    patient_db[patient_id]=patient.dict()
    return {'message': f'Successfully created patient: {patient_id}'}