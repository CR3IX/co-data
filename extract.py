import pandas as pd
import json
from models import *
from copy import deepcopy
from question_paper import *

student_data: List[Student] = []

#verify these values everytime
headers = ["Sno", "Reg. Number", "Section", "Name"]
total_co = 6
total_serial_tests = 3
total_assignments = 2

def get_all_co(df, serial_test : bool = True):
    if serial_test:
        return df.filter(like='co').iloc[:, :total_co * total_serial_tests]
    else:
        return df.filter(like='co').iloc[:, total_co * total_serial_tests : total_co * (total_serial_tests + total_assignments)]


def get_student_co_marks(df: pd.DataFrame, index: int, serial_test : bool = True):
    all_co = get_all_co(df, serial_test)
    return all_co.iloc[index, :]


def get_total_mark_co(df: pd.DataFrame, index: int, serial_test : bool = True):
    try:
        row = get_student_co_marks(df, 0, serial_test)
        return int(row[index])
    except BaseException:
        return 0


def populate_student_data(df: pd.DataFrame):
    for index, row in df.iterrows():
        if index == 0 or pd.isna(row[headers[1]]) or row[headers[1]] == "" or int(row[headers[1]]) == 0:
            continue
        reg_no = str(int(row[headers[1]]))
        section = str(row[headers[2]])
        name = str(row[headers[3]])

        student_co_marks_serial_test = get_student_co_marks(df, index)
        student_co_marks_assignments = get_student_co_marks(df, index, False)
        try:
            cos: List[Co] = []
            serial_tests: List[SerialTest] = []

            cos = []
            col_num = 0
            for col_name, value in student_co_marks_serial_test.items():
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
            
            cos = []
            col_num = 0
            for col_name, value in student_co_marks_assignments.items():
                co = Co(
                    num=int(col_name.removeprefix("co")[0]),
                    total_mark=get_total_mark_co(df, col_num, False),
                    obtained_mark=int(value)
                )
                cos.append(co)
                col_num += 1

            assignments = [SerialTest(
                num=i // 6 + 1,
                co=cos[i:i + 6]
            ) for i in range(0, len(cos), 6)]

            student = Student(
                reg_no=reg_no,
                section=section,
                name=name,
                serial_tests=serial_tests,
                assignments=assignments
            )
            student_data.append(student)
        except Exception as e:
            print(e)


def populate_questions_in_serial_test(qp, serial_test_index: int, serial_test : bool = True):
        base_questions = [Question.from_parsed_question(question) for question in qp["questions"][serial_test_index]]

        for student in student_data:
            # Create a deep copy of questions for each student
            if serial_test:
                student.serial_tests[serial_test_index].questions = deepcopy(base_questions)
            else:
                student.assignments[serial_test_index].questions = deepcopy(base_questions)


def populate_student_data_and_questions(df: pd.DataFrame):
    populate_student_data(df)
    qp = {"questions": [generate_questions(
            [co.model_dump() for co in serial_test.co], True
        ) for serial_test in student_data[0].serial_tests]}

    assignment_qp = {"questions": [generate_questions(
            [co.model_dump() for co in serial_test.co], False
        ) for serial_test in student_data[0].assignments]}

    for i in range(len(student_data[0].serial_tests)):
        populate_questions_in_serial_test(qp, i, True)

    for i in range(len(student_data[0].assignments)):
        populate_questions_in_serial_test(assignment_qp, i, False)

    lst = [
        student.model_dump() for student in student_data
    ]
    with open("student_data.json", "w") as f:
        json.dump(lst, f, indent=4)
    

    return student_data
