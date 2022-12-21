from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship,Mapped
from database import Base

class Students(Base):
    __tablename__ = "signup_students"

    # id = Column(Integer,index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    Age = Column(Integer)
    Gender = Column(String)
    Address_line_1 = Column(String)
    Address_line_2 = Column(String)
    City = Column(String)
    State = Column(String)
    Pincode= Column(Integer)
    Country = Column(String)
    Phone = Column(Integer,nullable=False,primary_key=True)
    email = Column(String,nullable=False)

    food_consumed=relationship("Consumption",back_populates="user")


class Consumption(Base):
    __tablename__ = "food_consumed"
   
    student_phone = Column(Integer,ForeignKey("signup_students.Phone",ondelete="CASCADE"),primary_key=True,nullable=False) 
    date = Column(String)
    type = Column(String)
    total_calories = Column(Integer)

    user=relationship("Students",back_populates="food_consumed")
    



