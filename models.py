from typing import List, Optional
import pydantic

class BaseModel(pydantic.BaseModel):
    pass

class Student(BaseModel):
    reg_no: str
    section: str
    name: str
    serial_tests: Optional[List["SerialTest"]] = None
    serial_tests_with_questions: Optional[List["SerialTestWithQuestions"]] = None

class SerialTestWithQuestions(BaseModel):
    num: int
    questions: List["Question"]

class Question(BaseModel):
    num: int
    option: str
    sub_division: str
    co: List["Co"]
    total_mark: int
    obtained_mark: int

class SerialTest(BaseModel):
    num: int
    co: List["Co"]

class Co(BaseModel):
    num: int
    total_mark: int
    obtained_mark: int
    