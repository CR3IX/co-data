import pandas as pd

def clean_header(df: pd.DataFrame) -> pd.DataFrame:
    sno_row_index = df[df.iloc[:, 0] == "Sno"].index[0]
    df.columns = df.iloc[sno_row_index]
    subject_details = df.iloc[:sno_row_index, :]
    df = df.iloc[sno_row_index+1:, :]

    return subject_details, df
