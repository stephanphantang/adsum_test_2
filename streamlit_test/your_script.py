#In this file, we realize the first test to get used with fastAPI
#import all the needed module
import streamlit as st
import requests
import json
import pickle

#We load here the list of symptom taken in account by the model
list_of_symptom = pickle.load(open("list_symptoms.sav","rb"))

#Display the title
st.title("Adsum test")

#input here the name of the new patient
patient_name = st.text_input('new patient name')

#here to select the symptom of the new patient, to change to accept more than one symptom
symptoms = st.multiselect('Pick symptoms', list_of_symptom) 

#We create from previous information a new patient under a dictionnary form
new_patient = {"patient_id": patient_name, "symptom": symptoms}

#Here we add the new patient by requesting the POST function from the API that allows us to create a new patient
if st.button("create new patient"):
    res = requests.post(url = "http://127.0.0.1:8000/patients", data= json.dumps(new_patient))
    st.subheader(f"new patient created = {res.text}")

#We request the get function of the API to display the patient database
if st.button("display patient list"):
    patient_list= requests.get("http://127.0.0.1:8000/patients")
    st.write(patient_list.text)

#here we predict a patient disease
patient_predict_id = st.text_input('name a patient you wish to predict the disease')
symptoms_to_predict = st.multiselect('Pick symptoms to obtain a disease', list_of_symptom)
predicted_patient ={"patient_id": patient_predict_id ,"symptom": symptoms_to_predict}
 
if st.button("display the predicted disease"):
    patient_predicted_disease = requests.get('http://127.0.0.1:8000/patients/{patient_id}/predict', data= json.dumps(predicted_patient))
    st.write(patient_predicted_disease.text)

print(requests.__version__)