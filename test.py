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

def test_student_data(student_data):
  for student in student_data:
    check_co_wise_total(student)
  

def test_question_paper(questions: List, co_marks_splitUp):
    # Step 1: Group questions by CO
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
        
        status = "✅ Matched" if assigned_marks == expected_marks else f"❌ Mismatch  {assigned_marks}"
        
        print(f"CO {co_num}: Assigned = {assigned_marks}, Expected = {expected_marks} --> {status}")
    
    print("\n===== Questions Grouped by CO =====")
    for co, q_list in same_co_questions.items():
        print(f"CO {co}:")
        for q in q_list:
            print(f"  - Q{q['no']} | Marks: {q['marks']} | Option: {q['option']}")
    
    return co_marks_assigned

# # Input Data
# questions = [
#     {"co": "2", "marks": 2, "option": None, "subDivision": None, "no": 1},
#     {"co": "2", "marks": 2, "option": None, "subDivision": None, "no": 2},
#     {"co": "2", "marks": 2, "option": None, "subDivision": None, "no": 3},
#     {"co": "2", "marks": 2, "option": None, "subDivision": None, "no": 4},
#     {"co": "2", "marks": 2, "option": None, "subDivision": None, "no": 5},
#     {"co": "3", "marks": 2, "option": None, "subDivision": None, "no": 6},
#     {"co": "3", "marks": 2, "option": None, "subDivision": None, "no": 7},
#     {"co": "3", "marks": 2, "option": None, "subDivision": None, "no": 8},
#     {"co": "3", "marks": 2, "option": None, "subDivision": None, "no": 9},
#     {"co": "3", "marks": 2, "option": None, "subDivision": None, "no": 10},
#     {"co": "1", "marks": 10, "option": "A", "subDivision": None, "no": 11},
#     {"co": "1", "marks": 10, "option": "B", "subDivision": None, "no": 11},
#     {"co": "1", "marks": 10, "option": "A", "subDivision": None, "no": 12},
#     {"co": "1", "marks": 10, "option": "B", "subDivision": None, "no": 12},
#     {"co": "2", "marks": 10, "option": "A", "subDivision": None, "no": 13},
#     {"co": "2", "marks": 10, "option": "B", "subDivision": None, "no": 13}
# ]

# co_marks_splitUp = [ 
#     {"num": 1, "total_mark": 20},
#     {"num": 2, "total_mark": 20},
#     {"num": 3, "total_mark": 10},
#     {"num": 4, "total_mark": 0},
#     {"num": 5, "total_mark": 0},
#     {"num": 6, "total_mark": 0}
# ]

# # Run validation
# test_question_paper(questions, co_marks_splitUp)