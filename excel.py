import pandas as pd

def clean_header(df: pd.DataFrame) -> pd.DataFrame:
    sno_row_index = df[df.iloc[:, 0] == "Sno"].index[0]
    df.columns = df.iloc[sno_row_index]
    subject_details = df.iloc[:sno_row_index-1, :]
    df = df.iloc[sno_row_index+1:, :]

    return subject_details, df

def merge_subjectdetails_studentdata(subject_details: pd.DataFrame, student_data: pd.DataFrame, output_filename: str) -> None:
    with pd.ExcelWriter(output_filename, engine="openpyxl") as writer:
        subject_details.to_excel(writer, index=False,header=False, sheet_name="Sheet1", startrow=1)
        student_data.to_excel(writer, index=False, sheet_name="Sheet1", startrow=len(subject_details) + 3)

    print(f"Excel file '{output_filename}' created successfully!")