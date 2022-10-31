# ADSUM - Help to diagnosis application

## Tables of contents

* [Objectives](#Objectives)
* [Technologies](#Technologies)
* [Launch](#Launch)

## Objectives

Help to diagnosis app, to save time to physician.
The app is based on a machine learning algorithm, which takes as input the observed symptoms on the patient and it should returns the possible disease that the patient has according 
to its symptoms.

## Technologies

### Programming languages
Python 3.8.5

### Python libraries used

FastAPI 0.85.1  
Pydantic 1.10.2  
Streamlit 1.13.0  
Requests 2.24.0  
json 2.0.9  

## Launch

To launch the application, first open your console at the localization of the fastapi_test directory and run the following command : "uvicorn main:app --reload".
This should launch the application backend.  
Then to open the frontend, open a second time your console at the localization of the streamlit_test directory and run the following command : "streamlit run your_script.py".
This will launch the application on your browser.
