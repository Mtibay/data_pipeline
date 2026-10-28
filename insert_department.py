
from snowflake_connection import conn

departments = [
    {
        "DEPARTMENT_ID": 101,
        "DEPARTMENT_NAME": "Information Technology",
        "DEPARTMENT_HEAD": "Juan Dela Cruz",
        "LOCATION": "Manila",
        "BUDGET": 2500000.00,
        "CREATED_AT": "2026-10-01 09:00:00"
    },
    {
        "DEPARTMENT_ID": 102,
        "DEPARTMENT_NAME": "Human Resources",
        "DEPARTMENT_HEAD": "Maria Santos",
        "LOCATION": "Cebu",
        "BUDGET": 1200000.00,
        "CREATED_AT": "2026-10-05 10:30:00"
    },
    {
        "DEPARTMENT_ID": 103,
        "DEPARTMENT_NAME": "Finance",
        "DEPARTMENT_HEAD": "Pedro Reyes",
        "LOCATION": "Davao",
        "BUDGET": 1800000.00,
        "CREATED_AT": "2026-10-10 14:15:00"
    },
    {
        "DEPARTMENT_ID": 104,
        "DEPARTMENT_NAME": "Operations",
        "DEPARTMENT_HEAD": "Ana Garcia",
        "LOCATION": "Batangas",
        "BUDGET": 3200000.00,
        "CREATED_AT": "2026-10-15 08:45:00"
    },
    {
        "DEPARTMENT_ID": 105,
        "DEPARTMENT_NAME": "Marketing",
        "DEPARTMENT_HEAD": "Mark Reyes",
        "LOCATION": "Quezon City",
        "BUDGET": 950000.00,
        "CREATED_AT": "2026-10-20 11:20:00"
    }
]

try:
    with conn.cursor() as cur:
        sql = """
            INSERT INTO IT_DEPARTMENT (
                DEPARTMENT_ID,
                DEPARTMENT_NAME,
                DEPARTMENT_HEAD,
                LOCATION,
                BUDGET,
                CREATED_AT
            )
            VALUES (%a, %s, %s, %s, %s, %s)
        """

        rows = [
            (
                d["DEPARTMENT_ID"],
                d["DEPARTMENT_NAME"],
                d["DEPARTMENT_HEAD"],
                d["LOCATION"],
                d["BUDGET"],
                d["CREATED_AT"]
            )
            for d in departments
        ]

        cur.executemany(sql, rows)
        print(f"Inserted {len(rows)} departments.")

finally:
    cur.close()
    conn.close()
