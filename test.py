from models import *
from copy import deepcopy


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

def check_co_wise_total(student: Student, cos: List[Co], questions: List[Question], num: int, serial_test: bool = True):
    for co in cos:
      co_questions = get_questions_with_co(questions, co)

      if not check_obtained_marks(co_questions, co):
        raise Exception(f"obtained_mark not matched {student.name} {'serial_test' if serial_test else 'assignment'}{num} co{co.num}")

      if not check_total_marks(co_questions, co):
        raise Exception(f"total_mark not matched {student.name} {'serial_test' if serial_test else 'assignment'}{num} co{co.num}")

    for question in questions:
      if question.obtained_mark > question.total_mark:
        print(f"obtained_mark exceeds total_mark {student.name} {'serial_test' if serial_test else 'assignment'}{num} co{co.num}")

def test_student_data(student_data):
  for student in student_data:
    for serial_test in student.serial_tests:
      check_co_wise_total(student, serial_test.co, serial_test.questions, serial_test.num, True)

    for assignment in student.assignments:
      check_co_wise_total(student, assignment.co, assignment.questions, assignment.num, False)
  

def test_question_paper(questions: List, co_marks_splitUp:List):
    # Step 1: Group questions by CO
    print("\n===== Testing Question Paper =====")
    same_co_questions = {}
    for question in questions:
        if question['co'] not in same_co_questions:
            same_co_questions[question['co']] = []
        same_co_questions[question['co']].append(question)
    
    # Step 2: Calculate total marks assigned per CO
    co_marks_assigned = {str(co["num"]): 0 for co in co_marks_splitUp}
    
    for co, q_list in same_co_questions.items():
        total_marks = sum(q["marks"] for q in q_list if q["option"] is None or q["option"] == "A")
        co_marks_assigned[co] = total_marks 
    
    print("\n===== CO Marks Validation =====")
    for co in co_marks_splitUp:
        co_num = str(co["num"])  
        expected_marks = co["total_mark"]
        assigned_marks = co_marks_assigned.get(co_num, 0)
        print(co,"co_num",co_num,"Assigned Marks:", assigned_marks, "Expected Marks:", expected_marks) 
        status = "✅ Matched" if assigned_marks == expected_marks else f"❌ Mismatch  {assigned_marks}"
        
        print(f"CO {co_num}: Assigned = {assigned_marks}, Expected = {expected_marks} --> {status}")
    
    print("\n===== Questions Grouped by CO =====")
    for co, q_list in same_co_questions.items():
        print(f"CO {co}:")
        for q in q_list:
            print(f"  - Q{q['no']} | Marks: {q['marks']} | Option: {q['option']}")
    
    return co_marks_assigned