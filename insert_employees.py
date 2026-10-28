from snowflake_connection import conn
import pandas as pd
from pandas.api.types import is_numeric_dtype

cur = conn.cursor()
df = pd.read_csv("employees_raw.csv")

# print(df.shape)
cur.execute("""
        SELECT COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE
        FROM Project1_DB.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'DEPARTMENT'
          AND TABLE_NAME = 'EMPLOYEE'
        ORDER BY ORDINAL_POSITION
    """)

metadata = cur.fetchall()
snowflake_columns = [row[0] for row in metadata]
snowflake_num_column = len(snowflake_columns)
df_column_num = df.shape[1]
df = df.drop(df[
    df["FIRST_NAME"].isnull() |
    df["LAST_NAME"].isnull() |
    (df["SALARY"] <= 0) |
    # (is_numeric_dtype(df["DEPARTMENT_ID"]) == False) |
    (pd.to_datetime(df["HIRE_DATE"]) > pd.Timestamp.today())
    ].index)
if snowflake_num_column == df_column_num:
    # Duplicate PK check
    # df = df[df.duplicated(subset=["EMPLOYEE_ID"], keep=False)]
    df["FULL_NAME"] = (
        df["FIRST_NAME"] +" "+ df["LAST_NAME"]
    )
    df["IS_LATEST"] = (
    df.groupby("EMPLOYEE_ID")["CREATED_AT"]
      .transform("max")
      .eq(df["CREATED_AT"])
    )     
    df = df.drop_duplicates(
        subset=["EMPLOYEE_ID"],
        keep="first"
    )
    df_dedup = df.loc[df["IS_LATEST"] == True]
    df_dedup = df.drop(
        columns=["FULL_NAME", "IS_LATEST"]
    )
    print(df_dedup)
    
    data = [
        (
            row["EMPLOYEE_ID"],
            row["FIRST_NAME"],
            row["LAST_NAME"],
            row["EMAIL"],
            row["DEPARTMENT_ID"],
            row["JOB_TITLE"],
            row["SALARY"],
            row["HIRE_DATE"],
            row["LOCATION"],
            row["CREATED_AT"]
        )
        for _, row in df_dedup.iterrows()
    ]
    try:
        cur.executemany(
            """
            INSERT INTO EMPLOYEE (
                EMPLOYEE_ID,
                FIRST_NAME,
                LAST_NAME,
                EMAIL,
                DEPARTMENT_ID,
                JOB_TITLE,
                SALARY,
                HIRE_DATE,
                LOCATION,
                CREATED_AT
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            data
        )
        print(data)
        print(f"Successfully inserted")
    except Exception as e:
        print(f"Failed to insert EMPLOYEE_ID={row['EMPLOYEE_ID']}")
        print(f"Error: {e}")

    cur.close()

    # print(df)
    # check_dup = df.groupby("EMPLOYEE_ID").size()
    # print(check_dup.to_string())

    # Null checks
    # df[df["FIRST_NAME"].isnull()]

    # # Invalid salary
    # df[df["SALARY"] <= 0]

    # # Invalid date
    # df[df["HIRE_DATE"] > pd.Timestamp.today()]
