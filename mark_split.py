from extract import *
import random

df = pd.read_excel("Compiler Design 2022-23 Even CO-PO attainment (1).xlsx", sheet_name='S2')
student_data: List[Student] = populate_student_data_and_questions(df, "sample_qp.json")


def get_co_questions(questions: List[Question], co: Co):
    questions = [question for question in questions if question.co == co.num]

    random.shuffle(questions)
    # Group questions by their number and option
    question_groups = {}
    for question in questions:
        key = (question.num, question.option)
        if key not in question_groups:
            question_groups[key] = []
        question_groups[key].append(question)

    # Select one option per question number, ensuring all subdivisions are included
    filtered_questions: List[Question]= []
    seen_question_nums = set()

    for question in questions:
        if question.num in seen_question_nums:
            continue

        if question.option is not None:
            # For questions with options, keep all subdivisions of the same option
            seen_question_nums.add(question.num)

            # Add all questions with this number and option (including all subdivisions)
            option_questions = question_groups.get((question.num, question.option), [])
            filtered_questions.extend(option_questions)
        else:
            # For questions without options, just add them directly
            filtered_questions.append(question)

    return [filtered_question for filtered_question in filtered_questions if filtered_question.obtained_mark != filtered_question.total_mark]


def distribute_marks_random(questions: List[Question], marks_to_be_distributed: int, correct_strictly: bool = True):
    buffer_questions = []
    while marks_to_be_distributed != 0:

        if len(questions) == 0:
            if correct_strictly:
                distribute_marks_random(buffer_questions, marks_to_be_distributed, False)
                return
            else:
                raise Exception("No questions left for CO", marks_to_be_distributed)

        random_question = random.choice(questions)

        if not random_question.obtained_mark:
            random_question.obtained_mark = 1
        else:
            if random_question.obtained_mark != random_question.total_mark:
                random_question.obtained_mark += 1

        if random_question.obtained_mark == random_question.total_mark:
            questions.remove(random_question)
        elif random_question and correct_strictly and random_question.obtained_mark >= random_question.total_mark - random.randint(1, 2):
            buffer_questions.append(random_question)
            questions.remove(random_question)

        marks_to_be_distributed -= 1


def get_part_b_c_questions(questions: List[Question]) -> List[Question]:
    return [question for question in questions if question.total_mark > 2]


def get_percentage(total_mark: int, obtained_mark: int) -> int:
    return int((obtained_mark / total_mark) * 100)


def get_mark_with_percentage(total_mark: int, percentage: int) -> int:
    return int((total_mark * percentage) / 100)


def get_total_questions_mark(questions: List[Question]) -> int:
    return sum([question.total_mark for question in questions])

def get_question_key(question: Question, serial_test: SerialTest):
    return f"serial test {serial_test.num}\nq{question.num}{question.option if question.option else ''}{question.sub_division if question.sub_division else ''}\nco{question.co}"

def get_co_key(co: Co, serial_test: SerialTest):
    return f"serial test {serial_test.num}\nco{co.num}"

def convert_to_series(student: Student) -> pd.Series:
    data = {}
    
    data["reg_no"] = student.reg_no
    data["section"] = student.section
    data["name"] = student.name
    
    for serial_test in student.serial_tests:
        for question in serial_test.questions:
            key = get_question_key(question, serial_test)
            data[key] = question.obtained_mark
        for co in serial_test.co:
            key = get_co_key(co, serial_test)
            data[key] = co.obtained_mark

    return pd.Series(data)

def get_total_mark_row(serial_tests: List[SerialTest]):
    data = {
        "reg_no": "",
        "section": "",
        "name": "Total Marks",
    }
    for serial_test in serial_tests:
        for question in serial_test.questions:
            data[get_question_key(question, serial_test)] = question.total_mark
        for co in serial_test.co:
            data[get_co_key(co, serial_test)] = co.total_mark
    return pd.Series(data)

def populate_student_co_marks(questions: List[Question], co: Co):
    co_questions = get_co_questions(questions, co)

    obtained_mark = co.obtained_mark
    part_b_c_questions = get_part_b_c_questions(co_questions)
    obtained_percentage = get_percentage(co.total_mark, co.obtained_mark)
    part_b_c_mark_weighted = get_mark_with_percentage(
        get_total_questions_mark(part_b_c_questions),
        min(obtained_percentage + random.randint(5, 10), 100)
    )

    distribute_marks_random(part_b_c_questions, part_b_c_mark_weighted)
    obtained_mark -= part_b_c_mark_weighted
    distribute_marks_random(co_questions, obtained_mark)


for student in student_data:
    for serial_test in student.serial_tests:
        for co in serial_test.co:
            if co and co.obtained_mark and co.obtained_mark > 0:
                populate_student_co_marks(serial_test.questions, co)

f = open("temp.json", "w")

student_data_json = [student.model_dump() for student in student_data]
f.write(json.dumps(student_data_json[10:45], indent=4))
f.close()

df = pd.DataFrame([get_total_mark_row(student_data[0].serial_tests)]+[convert_to_series(student) for student in student_data])
df.to_excel("student_data.xlsx", index=False)
