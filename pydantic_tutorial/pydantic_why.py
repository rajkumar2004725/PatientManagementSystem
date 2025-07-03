def insert_patient_data(name:str,age:int):
    #type validation
    if type(name)==str and type(age)==int:
        #data validation
        if age<0:
            raise ValueError("age must be greater than 0")
            
        
        else:
            print("Valid data")
            print(name)
            print(age)
            print("insert into database")
           
    else:
        raise TypeError("incorrect data type")


insert_patient_data("raj",50)