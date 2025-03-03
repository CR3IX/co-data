import random
from models import *
from copy import deepcopy
from test import *
from collections import defaultdict


def generate_questions(co_marks_splitUp, is_serialtest):
    co_marks_splitUp_copy = deepcopy(co_marks_splitUp)

    if is_serialtest:
        question_splitUp = [
            {"mark": 2, "no_of_questions": 9},
            {"mark": 10, "no_of_questions": 2},
            {"mark": 12, "no_of_questions": 1}
        ]
    else:
        question_splitUp = [
            {"mark": 2, "no_of_questions": 10},
            {"mark": 10, "no_of_questions": 3},
        ]
    questions = []
    
    co_marks_sorted = sorted(co_marks_splitUp, key=lambda x: x["total_mark"], reverse=True)
    question_splitUp_sorted = sorted(question_splitUp, key=lambda x: x["mark"], reverse=True)
    
    for question_type in question_splitUp_sorted:
        mark = question_type["mark"]
        num_questions = question_type["no_of_questions"]
        
        for _ in range(num_questions):
            for co in co_marks_sorted:
                if co["total_mark"] >= mark:
                    co["total_mark"] -= mark
                    
                    questions.append({
                        "co": str(co["num"]),
                        "marks": mark,
                        "option": "A" if mark > 2 else None,
                        "subDivision": None,
                        "obatained_mark": None
                    })
                    
                    # If mark > 2, create another question with option "B"
                    if mark > 2:
                        questions.append({
                            "co": str(co["num"]),
                            "marks": mark,
                            "option": "B",
                            "subDivision": None,
                            "obatained_mark": None
                        })
                    break
    
    # Sort questions by marks in ascending order
    questions_sorted = sorted(questions, key=lambda x: x["marks"])
    
    questions_sorted = group_and_sort_questions(questions_sorted)
    
    # Assign question numbers sequentially
    question_no = 1
    for i in range(len(questions_sorted)):
        if questions_sorted[i]["option"] == "B":
            questions_sorted[i]["no"] = questions_sorted[i - 1]["no"]
        else:
            questions_sorted[i]["no"] = question_no
            question_no += 1 
    
    test_question_paper(questions_sorted,co_marks_splitUp_copy)
    return questions_sorted

def group_and_sort_questions(questions_sorted):
    grouped_questions = defaultdict(list)
    
    # Group questions by marks
    for question in questions_sorted:
        grouped_questions[question["marks"]].append(question)
    
    # Sort each group by CO number
    for mark in grouped_questions:
        grouped_questions[mark] = sorted(grouped_questions[mark], key=lambda x: int(x["co"]))
    
    # Convert to sorted list
    sorted_grouped_list = []
    for mark in sorted(grouped_questions.keys()):
        sorted_grouped_list.extend(grouped_questions[mark])
    
    return sorted_grouped_list

if __name__ == "__main__":
    co_marks_splitUp = [
        {"num": 1, "total_mark": 20},
        {"num": 2, "total_mark": 20},
        {"num": 3, "total_mark": 10},
        {"num": 4, "total_mark": 0},
        {"num": 5, "total_mark": 0},
        {"num": 6, "total_mark": 0}
    ]


    questions = generate_questions(co_marks_splitUp,True)
