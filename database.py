import sqlite3

DB_NAME = "financial_inclusion.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            survey_date TEXT NOT NULL,
            district TEXT NOT NULL,
            upazila TEXT NOT NULL,
            gender TEXT NOT NULL,
            age_group TEXT NOT NULL,
            household_size INTEGER NOT NULL,
            monthly_income REAL NOT NULL,
            employment_status TEXT NOT NULL,
            bank_account INTEGER NOT NULL,
            mobile_finance INTEGER NOT NULL,
            savings_amount REAL NOT NULL,
            loan_access INTEGER NOT NULL,
            loan_amount REAL NOT NULL,
            loan_source TEXT NOT NULL,
            loan_purpose TEXT NOT NULL,
            repayment_rate REAL NOT NULL,
            financial_literacy INTEGER NOT NULL,
            insurance_access INTEGER NOT NULL,
            formal_finance INTEGER NOT NULL,
            financial_vulnerability INTEGER NOT NULL,
            vulnerability_level TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM financial_records")

    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    data = [
        ("2026-08-01","Dhaka","Savar","Female","26-35",5,28500,"Self-employed",1,1,8500,1,65000,"Microfinance","Business",91,72,0,1,34,"Medium"),
        ("2026-08-02","Chattogram","Hathazari","Male","36-45",6,32000,"Private Job",1,1,12000,1,80000,"Bank","Housing",94,81,1,1,22,"Low"),
        ("2026-08-03","Rajshahi","Paba","Female","36-45",4,18500,"Self-employed",0,1,4200,1,45000,"Microfinance","Business",86,63,0,0,61,"High"),
        ("2026-08-04","Khulna","Dumuria","Male","46-55",5,21000,"Farmer",1,1,6500,1,55000,"Microfinance","Agriculture",89,69,0,1,48,"Medium"),
        ("2026-08-05","Barishal","Bakerganj","Female","26-35",7,16000,"Farmer",0,1,2500,1,38000,"Microfinance","Agriculture",78,55,0,0,73,"High"),
        ("2026-08-06","Sylhet","Beanibazar","Male","26-35",4,27500,"Private Job",1,1,9500,0,0,"None","None",0,76,1,1,27,"Low"),
        ("2026-08-07","Rangpur","Mithapukur","Female","46-55",6,14500,"Farmer",0,1,1800,1,32000,"Microfinance","Agriculture",81,48,0,0,79,"Critical"),
        ("2026-08-08","Mymensingh","Trishal","Male","36-45",5,22500,"Business",1,1,7200,1,60000,"Bank","Business",92,74,1,1,31,"Medium"),
        ("2026-08-09","Cumilla","Daudkandi","Female","26-35",4,19500,"Self-employed",0,1,3500,1,42000,"Microfinance","Business",87,61,0,0,65,"High"),
        ("2026-08-10","Dhaka","Keraniganj","Male","18-25",3,24000,"Private Job",1,1,11000,0,0,"None","None",0,84,1,1,19,"Low")
    ]

    cursor.executemany("""
        INSERT INTO financial_records (
            survey_date,
            district,
            upazila,
            gender,
            age_group,
            household_size,
            monthly_income,
            employment_status,
            bank_account,
            mobile_finance,
            savings_amount,
            loan_access,
            loan_amount,
            loan_source,
            loan_purpose,
            repayment_rate,
            financial_literacy,
            insurance_access,
            formal_finance,
            financial_vulnerability,
            vulnerability_level
        )
        VALUES (
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?
        )
    """, data)

    conn.commit()
    conn.close()


def get_all_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM financial_records
        ORDER BY financial_vulnerability DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_records_dataframe():
    import pandas as pd

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM financial_records",
        conn
    )

    conn.close()

    return df
