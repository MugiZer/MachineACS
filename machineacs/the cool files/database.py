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
        cr.execute("CREATE DATABASE machineacs")
    except Exception as e:
        cn.rollback()
        print(f"Database setup note: {e}")

    # Create the batch tracking table
    try:
        cr.execute("""CREATE TABLE IF NOT EXISTS cleaning_batches 
        (
            batch_id UUID PRIMARY KEY,
            status TEXT,
            start_time TIMESTAMP,
            error TEXT
        )""")
    except Exception as e:
        cn.rollback()
        print(f"Batch table setup error: {e}")
        
    # Create the individual dictionary job tracking table
    try:
        cr.execute("""CREATE TABLE IF NOT EXISTS dictionary_jobs 
        (
            job_id UUID PRIMARY KEY,
            batch_id UUID REFERENCES cleaning_batches(batch_id) ON DELETE CASCADE,
            status TEXT,
            processed_time TIMESTAMP,
            error_message TEXT
        )""")
    except Exception as e:
        cn.rollback()
        print(f"Dictionary jobs table setup error: {e}")
        
    try:
        cr.execute("""CREATE TABLE IF NOT EXISTS hashes 
        (
            hash_value TEXT PRIMARY KEY,
            job_id UUID REFERENCES dictionary_jobs(job_id) ON DELETE CASCADE,
            after_hash_value TEXT
        )""")
        # Ensure column exists if table was created by an older version
        cr.execute("ALTER TABLE hashes ADD COLUMN IF NOT EXISTS after_hash_value TEXT")
    except Exception as e:
        cn.rollback()
        print(f"Hashes table setup error: {e}")
        
    try:
        cr.execute("""CREATE TABLE IF NOT EXISTS rule_logs 
        (
            log_id SERIAL PRIMARY KEY,
            job_id UUID REFERENCES dictionary_jobs(job_id) ON DELETE CASCADE,
            rule_type TEXT,
            key_name TEXT,
            before_val TEXT,
            after_val TEXT
        )""")
    except Exception as e:
        cn.rollback()
        print(f"Rule logs table setup error: {e}")

    cn.autocommit = False

# Initialize the DB structure
create_db()

def populate_batch(batch_id: str, status: str, time: str, error: str):
    """Upserts the high-level batch execution state."""
    try:
        cr.execute("""
        INSERT INTO cleaning_batches (batch_id, status, start_time, error)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (batch_id) DO UPDATE SET
            status = EXCLUDED.status,
            start_time = EXCLUDED.start_time,
            error = EXCLUDED.error
        """, (batch_id, status, time, error))
        cn.commit()
    except Exception as e:
        cn.rollback()
        print(f"Populate batch error: {e}")
        raise

def register_dictionary_job(job_id: str, batch_id: str, status: str, time: str, error: str = None):
    """Registers an individual dictionary processing result."""
    try:
        cr.execute("""
        INSERT INTO dictionary_jobs (job_id, batch_id, status, processed_time, error_message)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (job_id) DO UPDATE SET
            status = EXCLUDED.status,
            processed_time = EXCLUDED.processed_time,
            error_message = EXCLUDED.error_message
        """, (job_id, batch_id, status, time, error))
        cn.commit()
    except Exception as e:
        cn.rollback()
        print(f"Register dictionary job error: {e}")
        raise

def insert_before_hash_value(job_id: str, before_hash_value: str):
    """Links Canonicalized JSON hash to a specific dictionary job."""
    try:
        cr.execute("""
        INSERT INTO hashes (hash_value, job_id)
        VALUES (%s, %s)
        ON CONFLICT (hash_value) DO UPDATE SET job_id = EXCLUDED.job_id
        """, (before_hash_value, job_id))
        cn.commit()
    except Exception as e:
        cn.rollback()
        print(f"Insert hash error: {e}")

def update_after_hash_value(job_id: str, after_hash_value: str):
    """Updates the row linked to job_id with the final post-cleaning hash value."""
    try:
        cr.execute("""
        UPDATE hashes
        SET after_hash_value = %s
        WHERE job_id = %s
        """, (after_hash_value, job_id))
        cn.commit()
    except Exception as e:
        cn.rollback()
        print(f"Update after-hash error: {e}")

def insert_rule_log(job_id: str, rule_type: str, key_name: str, before: str, after: str):
    """Inserts an audit log entry for a specific dictionary job."""
    try:
        cr.execute("""
        INSERT INTO rule_logs (job_id, rule_type, key_name, before_val, after_val)
        VALUES (%s, %s, %s, %s, %s)
        """, (job_id, rule_type, key_name, before, after))
        cn.commit()
    except Exception as e:
        cn.rollback()
        print(f"Insert rule log error: {e}")

def get_matching_batch(batch_id: str):
    try:
        cr.execute("SELECT batch_id, status, start_time FROM cleaning_batches WHERE batch_id = %s", (batch_id,))
        result = cr.fetchone()
        if result:
            return {
                "id": str(result[0]),
                "status": result[1],
                "time": str(result[2])
            }
    except Exception as e:
        cn.rollback()
        print(f"Get batch error: {e}")
    return None

def close_session():
    cr.close()
    cn.close()
