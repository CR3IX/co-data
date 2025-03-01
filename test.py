from mark_split import *
from models import *

def get_questions_with_co(questions: List[Question], co: Co):
  return [question for question in questions if question.co == co.num]

def check_obtained_marks(questions: List[Question], co:Co):
  obtained_total = sum([question.obtained_mark for question in questions])
  return obtained_total == co.obtained_mark

def check_total_marks(questions: List[Question], co:Co):
  questions_copy = [deepcopy(question) for question in questions]
  
  for question in questions_copy:
    if question.option and question.option != "A":
      questions_copy.remove(question)

  total_mark = sum([question.total_mark for question in questions_copy])
  return total_mark == co.total_mark

def check_co_wise_total(student: Student):
  for serial_test in student.serial_tests:
    
    for co in serial_test.co:
      co_questions = get_questions_with_co(serial_test.questions, co)

      if not check_obtained_marks(co_questions, co):
        print(f"obtained_mark not matched {student.name} serial_test{serial_test.num} co{co.num}")

      if not check_total_marks(co_questions, co):
        print(f"total_mark not matched {student.name} serial_test{serial_test.num} co{co.num}")

    for question in serial_test.questions:
      if question.obtained_mark > question.total_mark:
        print(f"obtained_mark exceeds total_mark {student.name} serial_test{serial_test.num} co{co.num}")

for student in student_data:
  check_co_wise_total(student)

      