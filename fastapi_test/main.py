#In this file, we realize the first test to get used with fastAPI
#import all the needed module
from fastapi import FastAPI
from pydantic import BaseModel
import pickle

#We load here the machine learning model of ADSUM, it is a random forest classifier with a Bayes optimization.
#This model will predict a disease based on a given list of symptoms
loaded_model = pickle.load(open("adsum_model.sav", 'rb'))

#we create here a class Patient, for now it contains name and symptoms.
#In future,name should be replace by a numerical id and add a disease part
#Moreover, symptom should be a list for next time
class Patient(BaseModel):
    patient_id: str
    symptom: str

#call the function fastAPI
app = FastAPI()

#instantiate a temporary patient database for the test
patient_db ={
    'jack': {"patient_id": 'jack', "symptom": "fever"},
    'jill': {"patient_id": 'jill', "symptom": "scratch"},
    'jane': {"patient_id": 'jane', "symptom": "vomiting"}
    }

#this function is to obtain the patient database
@app.get("/patients")
def get_patients():
    patient_list= list(patient_db.values())
    return patient_list

#this function is to obtain data on a particular patient, based on his name
@app.get("/patients/{patient_id}")
def get_(patient_id: str):
    return patient_db[patient_id]

#This function is to add a new patient in the database
@app.post('/patients')
def create_patient(patient: Patient):
    patient_id= patient.patient_id
    patient_db[patient_id]=patient.dict()
    return {'message': f'Successfully created patient: {patient_id}'}

