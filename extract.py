import pandas as pd
import json
from models import *
from copy import deepcopy

student_data: List[Student] = []

headers = ["Sno", "Reg. Number", "Section", "Name"]
total_co = 6


def get_all_co(df):
    return df.filter(like='co').iloc[:, :total_co * 3]


def get_student_co_marks(df: pd.DataFrame, index: int):
    all_co = get_all_co(df)
    return all_co.iloc[index, :]


def get_total_mark_co(df: pd.DataFrame, index: int):
    try:
        row = get_student_co_marks(df, 0)
        return int(row[index])
    except BaseException:
        return 0


def populate_student_data(df: pd.DataFrame):
    for index, row in df.iterrows():
        if index == 0:
            continue
        reg_no = str(int(row[headers[1]]))
        section = str(row[headers[2]])
        name = str(row[headers[3]])

        student_co_marks = get_student_co_marks(df, index)
        try:
            cos: List[Co] = []
            serial_tests: List[SerialTest] = []

            cos = []
            col_num = 0
            for col_name, value in student_co_marks.items():
                co = Co(
                    num=int(col_name.removeprefix("co")[0]),
                    total_mark=get_total_mark_co(df, col_num),
                    obtained_mark=int(value)
                )
                cos.append(co)
                col_num += 1

            serial_tests = [SerialTest(
                num=i // 6 + 1,
                co=cos[i:i + 6]
            ) for i in range(0, len(cos), 6)]

            student = Student(
                reg_no=reg_no,
                section=section,
                name=name,
                serial_tests=serial_tests
            )
            student_data.append(student)
        except Exception as e:
            print(e)


def populate_questions_in_serial_test(question_paper_json_file_name: str, serial_test_index: int):
    with open(question_paper_json_file_name, "r") as f:
        qp = json.load(f)
        base_questions = [Question.from_parsed_question(question) for question in qp["questions"][serial_test_index]]

        for student in student_data:
            # Create a deep copy of questions for each student
            student.serial_tests[serial_test_index].questions = deepcopy(base_questions)


def populate_student_data_and_questions(df: pd.DataFrame, question_paper_json_file_name: str):
    populate_student_data(df)

    for i in range(len(student_data[0].serial_tests)):
        populate_questions_in_serial_test(question_paper_json_file_name, i)

    return student_data
