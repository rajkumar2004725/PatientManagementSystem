from fastapi import FastAPI, Path ,HTTPException ,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import copy


app =FastAPI()    

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="The unique ID of the patient", example='P001')]
    name:Annotated[str,Field(...,description="name of the patient")]
    city:Annotated[str,Field(...,description="city of the patient")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="age of the patient")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="select the gender of the patient")]
    
    height:Annotated[float,Field(...,gt=0,description="height of the patient in meters")]
    weight:Annotated[float,Field(...,gt=0,description="bmi of the patient in kg")]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi <= 24.9:
            return "Normal weight"
        elif 25 <= self.bmi <=29.9:
            return "Overweight"
        else:
            return "Obesity"



class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None)]
    gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]




#now save data
def save_data(data):
    with open("patients.json",'w') as f:
        json.dump(data,f)


def load_data():
    with open ("patients.json",'r') as f:
        data =json.load(f)
    return data






@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists") 
    
    data[patient.id] = patient.model_dump(exclude=['id'])  # Save rest of the fields
    save_data(data)

    return JSONResponse(
        status_code=201, 
        content={"message": "Patient created successfully", "patient_id": patient.id}
    )




@app.get("/")
def hello():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patients records"}


@app.get('/view')
def view():
    data=load_data()
    return data



@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to view", example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient ID not found")


@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description="Sort on the basis of height,weight or bmi"),order:str=Query('asc',description="sort in asc or desc order")):
    valid_feilds =['height','weight','bmi']
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400,details=f'Invalid sort field. Valid fields are {valid_feilds}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,details='Invalid order. Valid orders are asc or desc')
    
    data=load_data()

    sort_order = True if order==True else False 

    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data

"""existing patient info ->pydantic object ->update bmi and verdict -> (pydantic to dict) -> update the data dict -> save the data dict to file"""

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID not found")

    # Update the existing patient data with the new values
    existing_patient_data = data[patient_id]

    patient_update_data = patient_update.model_dump(exclude_unset=True)

    for key,value in patient_update_data.items():
        if value is not None:
            existing_patient_data[key] = value


    existing_patient_data['id'] = patient_id
    patient_pydatntic_obj=Patient(**existing_patient_data) 

    existing_patient_data= patient_pydatntic_obj.model_dump(exclude=['id'])
    # Save the updated data back to the file
    data[patient_id] = existing_patient_data
    save_data(data)
    return JSONResponse(
        status_code=200,
        content={"message": "Patient updated successfully", "patient_id": patient_id}
    )




@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient ID not found")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient deleted successfully", "patient_id": patient_id}
    )
