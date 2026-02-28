import psycopg2

def start_session():
    # Helper to get a cursor
    global cn, cr
    cn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="hamza158",
        dbname="postgres",
        port="5432"
    )
    cr = cn.cursor()

# Global connection/cursor for the app
cn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="hamza158",
    dbname="postgres",
    port="5432"
)
cr = cn.cursor()

def create_db():
    cn.autocommit = True
    try:
        # Note: 'IF NOT EXISTS' is not standard Postgres for CREATE DATABASE
        # We catch the error instead.
        cr.execute("CREATE DATABASE machineacs")
    except Exception as e:
        # If it already exists, Postgres might abort the transaction
        # even in autocommit mode for some errors, so we rollback just in case.
        cn.rollback()
        print(f"Database setup note: {e}")

    try:
        cr.execute("""CREATE TABLE IF NOT EXISTS jobs 
        (
            job_id UUID PRIMARY KEY,
            status TEXT,
            time TIMESTAMP,
            error TEXT
        )""")
    except Exception as e:
        cn.rollback()
        print(f"Table setup error: {e}")

    cn.autocommit = False

# Initialize the DB structure
create_db()

def populate_db(job_id: str, status: str, time: str, error: str):
    try:
        cr.execute("""
        INSERT INTO jobs (job_id, status, time, error)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (job_id) DO UPDATE SET
            status = EXCLUDED.status,
            time = EXCLUDED.time,
            error = EXCLUDED.error
        """, (job_id, status, time, error))
        cn.commit()
    except Exception as e:
        cn.rollback()
        print(f"Populate DB error: {e}")
        raise

def get_matching_job(id: str):
    try:
        cr.execute("SELECT job_id, status, time FROM jobs WHERE job_id = %s", (id,))
        result = cr.fetchone()
        if result:
            return {
                "id": str(result[0]),
                "status": result[1],
                "time": str(result[2])
            }
    except Exception as e:
        cn.rollback()
        print(f"Get job error: {e}")
    return None

def get_job_by_status(status_val: str):
    try:
        cr.execute("SELECT job_id, status, time FROM jobs WHERE status = %s", (status_val,))
        result = cr.fetchone()
        if result:
            return {
                "id": str(result[0]),
                "status": result[1],
                "time": str(result[2])
            }
    except Exception as e:
        cn.rollback()
        print(f"Get job by status error: {e}")
    return None

def close_session():
    cr.close()
    cn.close()
