from snowflake_connection import conn

with conn.cursor() as cur:
    sql = "SELECT * FROM IT_DEPARTMENT"

    cur.execute(sql)
    # data = cur.fetchall()
    # print(data[1][5])
    while True:
        row = cur.fetchone()
        print(row)
        if row is None:
            break