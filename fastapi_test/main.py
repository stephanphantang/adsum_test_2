#In this file, we realize the first test to get used with fastAPI
#import all the needed module
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from typing import List
import pandas as pd
import numpy as np


#We load here the machine learning model of ADSUM, it is a random forest classifier with a Bayes optimization.
#This model will predict a disease based on a given list of symptoms
loaded_model = pickle.load(open("adsum_model.sav", 'rb'))

#We load here the list of symptom taken in account by the model
list_of_symptom = pickle.load(open("list_symptoms.sav","rb"))

#we create here a class Patient, for now it contains name and symptoms.
#In future,name should be replace by a numerical id and add a disease part
#Moreover, symptom should be a list for next time
class Patient(BaseModel):
    patient_id: str
    symptom: List[str]

#call the function fastAPI
app = FastAPI()

#instantiate a temporary patient database for the test
patient_db ={
    'jack': {"patient_id": 'jack', "symptom": [" fever"]},
    'jill': {"patient_id": 'jill', "symptom": [" scratch"]},
    'jane': {"patient_id": 'jane', "symptom": [" vomiting"]}
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

#this function aim to convert the list of symptoms into a one hot encoding table processable for the model
def treat_patient(symptom_list, table_symptom):
    my_zero_list= [0]*len(table_symptom.columns)
    table_symptom=table_symptom.append(pd.Series(my_zero_list,index=table_symptom.columns), ignore_index=True)
    for symptom in symptom_list:
        if symptom in table_symptom.columns:
            table_symptom.at[0,symptom]=1
        elif " "+symptom in table_symptom.columns:
            table_symptom.at[0," "+symptom]=1
    return table_symptom

#this function is for displaying the most probable class predicted and their probabilities (3 most probable for now)
def display_max(class_list, proba_list):
    sorted_proba= sorted(proba_list,reverse=True)
    most_proba_id= proba_list.index(sorted_proba[0])
    sec_proba_id= proba_list.index(sorted_proba[1])
    third_proba_id= proba_list.index(sorted_proba[2])
    return [(class_list[most_proba_id],sorted_proba[0]),(class_list[sec_proba_id],sorted_proba[1]),(class_list[third_proba_id],sorted_proba[2])]

#This function will predict the disease of a given patient
@app.get("/patients/{patient_id}/predict")
def predict_patient_disease(patient: Patient):
    symptoms= patient.symptom
    empty_symptom_table= pd.DataFrame(columns=list_of_symptom)
    ohe_symptom_list= treat_patient(symptoms,empty_symptom_table)
    return display_max(loaded_model.classes_.tolist(), loaded_model.predict_proba(ohe_symptom_list).tolist()[0])


