from extract import *
import random
from test import *
import os
import threading
from excel import *

def generate_attainment_mark(attainment_file_path, file_name):

    df = pd.read_excel(attainment_file_path, sheet_name='S2')
    subject_details, students_data = clean_header(df)

    student_data: List[Student] = populate_student_data_and_questions(students_data)

    def filter_questions_choose_random_option(questions : List[Question]):
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

        return filtered_questions

    def get_co_questions(questions: List[Question], co: Co):
        questions = [question for question in questions if question.co == co.num]

        filtered_questions = filter_questions_choose_random_option(questions)

        return [filtered_question for filtered_question in filtered_questions if filtered_question.obtained_mark != filtered_question.total_mark]

    def distribute_marks_random(questions: List[Question], marks_to_be_distributed: int, co: Co, student: Student, correct_strictly: bool = True):
        buffer_questions = []
        while marks_to_be_distributed > 0:

            if len(questions) == 0:
                if correct_strictly and len(buffer_questions) > 0:
                    distribute_marks_random(buffer_questions, marks_to_be_distributed, co, student, False)
                    return
                else:
                    raise Exception(f"""No questions left for CO {co.num} for student {student.reg_no} {student.name} {marks_to_be_distributed}
                                    {co.obtained_mark}
                                    """)

            random_question = random.choice(questions)

            if not random_question.obtained_mark:
                random_question.obtained_mark = 1
            else:
                if random_question.obtained_mark < random_question.total_mark - (1 if correct_strictly else 0):
                    random_question.obtained_mark += 1

            if random_question.obtained_mark == random_question.total_mark - (1 if correct_strictly else 0):
                questions.remove(random_question)
                buffer_questions.append(random_question)

            marks_to_be_distributed -= 1

    def get_part_a_questions(questions: List[Question]):
        return [question for question in questions if question.total_mark <= 2]

    def get_part_b_c_questions(questions: List[Question]) -> List[Question]:
        return [question for question in questions if question.total_mark > 2]


    def get_percentage(total_mark: int, obtained_mark: int):
        if total_mark == 0:
            return 0
        return (obtained_mark / total_mark) * 100


    def get_mark_with_percentage(total_mark: int, percentage: int) -> int:
        mark = int((total_mark * percentage) / 100)
        return mark + (1 if mark < total_mark else 0)


    def get_total_questions_mark(questions: List[Question]) -> int:
        filtered_questions = filter_questions_choose_random_option(questions)

        return sum([question.total_mark for question in filtered_questions])

    def get_question_key(question: Question, serial_test: SerialTest, is_serial_test: bool = True):
        return f"{"serial test" if is_serial_test else "assignment"} {serial_test.num}\nq{question.num}{question.option if question.option else ''}{question.sub_division if question.sub_division else ''}\nco{question.co}"

    def get_co_key(co: Co, serial_test: SerialTest, is_serial_test: bool = True):
        return f"{"serial test" if is_serial_test else "assignment"} {serial_test.num}\nco{co.num}"

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

        for assignment in student.assignments:
            for question in assignment.questions:
                key = get_question_key(question, assignment, False)
                data[key] = question.obtained_mark
            for co in assignment.co:
                key = get_co_key(co, assignment, False)
                data[key] = co.obtained_mark

        return pd.Series(data)

    def get_total_mark_row(serial_tests: List[SerialTest], assignments: List[SerialTest]):
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
        for assignment in assignments:
            for question in assignment.questions:
                data[get_question_key(question, assignment, False)] = question.total_mark
            for co in assignment.co:
                data[get_co_key(co, assignment, False)] = co.total_mark
        return pd.Series(data)

    def populate_student_co_marks(questions: List[Question], co: Co, student: Student, serial_test: bool = True):
        co_questions = get_co_questions(questions, co)

        obtained_mark = co.obtained_mark
        
        part_b_c_questions = get_part_b_c_questions(co_questions)
        part_a_questions = get_part_a_questions(co_questions)

        if serial_test:
            obtained_percentage = get_percentage(co.total_mark, co.obtained_mark)
            part_b_c_mark_weighted = get_mark_with_percentage(
                get_total_questions_mark(part_b_c_questions),
                min(obtained_percentage + random.randint(0,5), 100)
            )
            # distribute_marks_random(co_questions, co.obtained_mark, )
            
            distribute_marks_random(part_b_c_questions, part_b_c_mark_weighted, co, student)
            obtained_mark -= part_b_c_mark_weighted
            distribute_marks_random(part_a_questions, obtained_mark, co, student)
        else:
            distribute_marks_random(co_questions, co.obtained_mark, co, student)


    for student in student_data:
        for serial_test in student.serial_tests:
            for co in serial_test.co:
                if co and co.obtained_mark and co.obtained_mark > 0:
                    if co.total_mark == 0:
                        print(f"student {student.reg_no} {student.name} co {co.num} total mark is 0 serial test")

                    co.obtained_mark = min(co.obtained_mark, co.total_mark)
                
                    populate_student_co_marks(serial_test.questions, co, student, True)

        for assignment in student.assignments:
            for co in assignment.co:
                if co and co.obtained_mark and co.obtained_mark > 0:
                    if co.total_mark == 0:
                        print(f"student {student.reg_no} {student.name} co {co.num} total mark is 0 assignment")

                    co.obtained_mark = min(co.obtained_mark, co.total_mark)

                    populate_student_co_marks(assignment.questions, co, student, False)

    f = open("temp.json", "w")

    student_data_json = [student.model_dump() for student in student_data]
    f.write(json.dumps(student_data_json[:45], indent=4))
    f.close()

    df = pd.DataFrame([get_total_mark_row(student_data[0].serial_tests, student_data[0].assignments)]+[convert_to_series(student) for student in student_data])
    merge_subjectdetails_studentdata(subject_details, df, f"Question {file_name[:-4]}.xlsx")

    test_student_data(student_data)
    
threads = []
attainment_folder_path = "THEORY"
files = sorted(os.listdir(attainment_folder_path))
for index,file_name in enumerate(files[2:3]):
    file_path = os.path.join("THEORY",file_name)
    print(file_path)
    generate_attainment_mark(file_path, file_name)
#     t = threading.Thread(target=generate_attainment_mark, args=(file_path, file_name))
#     threads.append(t)
#     t.start()

# for t in threads:
#     t.join()
