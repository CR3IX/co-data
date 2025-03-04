import pandas as pd
import os

def clean_header(df: pd.DataFrame) -> pd.DataFrame:
    sno_row_index = df[df.iloc[:, 0] == "Sno"].index[0]
    df.columns = df.iloc[sno_row_index]
    subject_details = df.iloc[:sno_row_index-1, :]
    students_data = df.iloc[sno_row_index+1:, :].reset_index(drop=True)
    
    students_data.fillna(0, inplace=True)

    return subject_details, students_data

def merge_subjectdetails_studentdata(subject_details: pd.DataFrame, student_data: pd.DataFrame, output_filename: str) -> None:
    output_filepath = os.path.join("output", output_filename)
    if not os.path.exists("output"):
        os.mkdir("output")
        
    with pd.ExcelWriter(output_filepath, engine="openpyxl") as writer:
        subject_details.to_excel(writer, index=False,header=False, sheet_name="Sheet1", startrow=1)
        student_data.to_excel(writer, index=False, sheet_name="Sheet1", startrow=len(subject_details) + 3)

    print(f"Excel file '{output_filename}' created successfully!")