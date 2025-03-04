import random
from models import *
from copy import deepcopy
from test import *
from collections import defaultdict
import json

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

def generate_questions(co_marks_splitUp, is_serialtest):
    co_marks_splitUp_copy = deepcopy(co_marks_splitUp)
    
    if is_serialtest:
        question_splitUp = [
            {"mark": 12, "no_of_questions": 1},
            {"mark": 10, "no_of_questions": 2},
            {"mark": 2, "no_of_questions": 9}
        ]
    else:
        question_splitUp = [
            {"mark": 10, "no_of_questions": 3},
            {"mark": 2, "no_of_questions": 10}
        ]
    
    questions = []
    
    # Sort COs by total_mark in descending order
    co_marks_sorted = sorted(co_marks_splitUp, key=lambda x: x["total_mark"], reverse=True)
    
    def assign_questions():
        question_cycle = [q for q in question_splitUp for _ in range(q["no_of_questions"])]
        question_index = 0
        
        while any(co["total_mark"] > 0 for co in co_marks_sorted) and question_index < len(question_cycle):
            print(f"{any(co["total_mark"] > 0 for co in co_marks_sorted)}")
            for co in co_marks_sorted:
                if co["total_mark"] <= 0:
                    continue
                
                question_type = question_cycle[question_index]
                question_mark = question_type["mark"]
                
                if co["total_mark"] >= question_mark:
                    co["total_mark"] -= question_mark
                    questions.append({
                        "co": str(co["num"]),
                        "marks": question_mark,
                        "option": "A" if question_mark > 2 else None,
                        "subDivision": None,
                        "obtained_mark": None
                    })
                    
                    if question_mark > 2:
                        questions.append({
                            "co": str(co["num"]),
                            "marks": question_mark,
                            "option": "B",
                            "subDivision": None,
                            "obtained_mark": None
                        })
                    
                    question_index += 1
                    if question_index >= len(question_cycle):
                        break
                else:
                    print(f"co{co['num']} total mark {co['total_mark']} question mark {question_mark}")
    
    assign_questions()
    questions_sorted = sorted(questions, key=lambda x: x["marks"]) 
    questions_sorted = group_and_sort_questions(questions_sorted)
    
    # Assign question numbers
    question_no = 1
    for i in range(len(questions_sorted)):
        if questions_sorted[i]["option"] == "B":
            questions_sorted[i]["no"] = questions_sorted[i - 1]["no"]
        else:
            questions_sorted[i]["no"] = question_no
            question_no += 1 
    
    test_question_paper(questions_sorted, co_marks_splitUp_copy)
    return questions_sorted


if __name__ == "__main__":
    co_marks_splitUp = [
        {"num": 1, "total_mark": 10},
        {"num": 2, "total_mark": 10},
        {"num": 3, "total_mark": 30},
        {"num": 4, "total_mark": 0},
        {"num": 5, "total_mark": 0},
        {"num": 6, "total_mark": 0}
    ]

    questions = generate_questions(co_marks_splitUp,False)