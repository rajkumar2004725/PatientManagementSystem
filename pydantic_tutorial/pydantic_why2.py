from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated

#Field custom data validation condition
#data validation EmailStr,AnyUrl datatypes
class Patient(BaseModel):
    name:Annotated[str,Field(min_length=3,max_length=50,tittle="name of the patient",description="name must be between 3 to 50 characters",examples=["raj","pawan kumar","john doe"])]
    email:EmailStr
    age:int=Field(gt=0)
    url_input:AnyUrl
    weight:float=Annotated[float,Field(gt=0,lt=500,strict=True)]# strict=True means it will not accept string values so no conversion 
    married:Annotated[bool,Field(default=False,discription='is the patient married?',example=True)]
    allergies:Annotated[Optional[list[str]],Field(max_length=6)]
    contact_details:Dict[str,str]


class patient2(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    married:bool
    allergies:List[str]
    contact_details:Dict[str,str]


    #check if email contains hdfc or icici to conform he is a bank employee
    #@field_validator--->decorator
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icici.com']
        domain_name= value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Email must be from one of the following domains: {valid_domains}")
        return value
    
    #mode='before' means it will be applied before the validation (field validator)

    @field_validator('name',mode='before')#default mode is 'after'
    @classmethod
    def name_transform(cls,value):
        return value.upper()
    



def insert_patient_data(patient:patient2):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print("insert into database")

def update_patient_data(patient:patient2):
    print(patient.name)
    print(patient.age)
    print("update into database")

patient_info = {'age':20,'weight':64.6,
                'allergies':['dust','pollen'],'contact_details':{'email':'abc@gmail.com','phone':'8660661474'} }

# ** for unpacking the dictionary
patient1=patient2(**patient_info) #validation -->type coercion

insert_patient_data(patient1)
update_patient_data(patient1)