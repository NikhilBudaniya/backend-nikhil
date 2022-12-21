from pydantic import BaseModel, Field

class Student(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    password: str = Field(min_length=5)
    Age:int = Field()
    Gender: str = Field(min_length=1)
    Address_line_1: str = Field(min_length=1,max_length=100)
    Address_line_2: str = Field(max_length=100)
    City: str = Field(min_length=1)
    State: str = Field(min_length=1)
    Pincode: int = Field()
    Country: str = Field(min_length=1)
    Phone: int = Field()
    email: str = Field(min_length=1)
    DOB : str = Field(min_length=1)

class FoodConsumption(BaseModel):
    student_phone: int = Field()
    date: str= Field(min_length=1)
    type: str= Field(min_length=1)
    total_calories: int= Field()