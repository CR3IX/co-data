from typing import List, Optional
import pydantic
import pandas as pd

class BaseModel(pydantic.BaseModel):
    pass


class Student(BaseModel):
    reg_no: str
    section: str
    name: str
    serial_tests: Optional[List["SerialTest"]] = None
    assignments: Optional[List["SerialTest"]] = None


class Question(BaseModel):
    num: int
    option: Optional[str] = None
    sub_division: Optional[str] = None
    co: int
    total_mark: int
    obtained_mark: int

    @classmethod
    def from_parsed_question(cls, qp_parsed_question):
        return cls(
            num=int(qp_parsed_question["no"]),
            option=qp_parsed_question["option"] if qp_parsed_question["option"] is not None else None,
            sub_division=qp_parsed_question["subDivision"] if qp_parsed_question.get("subDivision") is not None else None,
            co=int(qp_parsed_question["co"]),
            total_mark=int(qp_parsed_question["marks"]),
            obtained_mark=0  # Assuming obtained_mark is set elsewhere
        )


class SerialTest(BaseModel):
    num: int
    co: List["Co"]
    questions: Optional[List["Question"]] = None


class Co(BaseModel):
    num: int
    total_mark: Optional[int] = None
    obtained_mark: Optional[int] = None
