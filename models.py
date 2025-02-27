from typing import List
import pydantic

class BaseModel(pydantic.BaseModel):
    pass

class Student(BaseModel):
    reg_no: str
    section: str
    name: str
    serial_test: List["SerialTest"]
    serial_test_with_questions: List["SerialTestWithQuestions"]

class SerialTestWithQuestions(BaseModel):
    questions: List["Question"]

class Question(BaseModel):
    num: int
    option: str
    sub_division: str
    co: List["Co"]
    total_mark: int
    obtained_mark: int

class SerialTest(BaseModel):
    co: List["Co"]

class Co(BaseModel):
    num: int
    total_mark: int
    obtained_mark: int
    