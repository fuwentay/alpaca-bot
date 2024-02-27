import psycopg2
from psycopg2 import sql
from datetime import datetime
import json

import os
from dotenv import load_dotenv
load_dotenv()


conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password=os.getenv("POSTGRES_PASSWORD"), port=5432)

# Logging of errors to "error_logs" table
def log_trade(error_source, error_message, error_details=None, error_severity="ERROR", user_id=None, session_id=None, request_id=None, additional_info=None):
    try:
        # Connect to your database
        cur = conn.cursor()

        # Create table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            error_id SERIAL PRIMARY KEY,
            error_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            error_source VARCHAR(255) NOT NULL,
            error_message TEXT NOT NULL,
            error_details TEXT,
            error_severity VARCHAR(50),
            user_id INT,
            session_id VARCHAR(255),
            request_id VARCHAR(255),
            additional_info JSONB
        );
        """)

        # Prepare the INSERT statement
        query = sql.SQL("""
        INSERT INTO error_logs (error_timestamp, error_source, error_message, error_details, error_severity, user_id, session_id, request_id, additional_info)
        VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s)
        """)
        
        # Convert additional_info to JSON string if it's not None
        additional_info_json = json.dumps(additional_info) if additional_info is not None else None

        # Execute the INSERT statement
        cur.execute(query, (error_source, error_message, error_details, error_severity, user_id, session_id, request_id, additional_info_json))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Failed to log error to database: {e}")
        # Handle failure to log to database (e.g., fallback to logging to a file)


# Logging of errors to "error_logs" table
def log_error(error_source, error_message, error_details=None, error_severity="ERROR", user_id=None, session_id=None, request_id=None, additional_info=None):
    try:
        # Connect to your database
        cur = conn.cursor()

        # Create table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            error_id SERIAL PRIMARY KEY,
            error_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            error_source VARCHAR(255) NOT NULL,
            error_message TEXT NOT NULL,
            error_details TEXT,
            error_severity VARCHAR(50),
            user_id INT,
            session_id VARCHAR(255),
            request_id VARCHAR(255),
            additional_info JSONB
        );
        """)

        # Prepare the INSERT statement
        query = sql.SQL("""
        INSERT INTO error_logs (error_timestamp, error_source, error_message, error_details, error_severity, user_id, session_id, request_id, additional_info)
        VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s)
        """)
        
        # Convert additional_info to JSON string if it's not None
        additional_info_json = json.dumps(additional_info) if additional_info is not None else None

        # Execute the INSERT statement
        cur.execute(query, (error_source, error_message, error_details, error_severity, user_id, session_id, request_id, additional_info_json))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Failed to log error to database: {e}")
        # Handle failure to log to database (e.g., fallback to logging to a file)

# # Example usage
# log_error(
#     error_source="MyApplication",
#     error_message="Example error message",
#     error_details="Detailed error information, stack trace, etc.",
#     additional_info={"module": "example_module", "action": "test_error_logging"}
# )


# Create table and insert data
def example_function():
    cur = conn.cursor()

    # database work
    cur.execute("""CREATE TABLE IF NOT EXISTS person (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        gender CHAR
    );
    """)    # this sends an SQL command to the database

    cur.execute("""INSERT INTO person (id, name, age, gender) VALUES
    (1, 'Mike', 30, 'm');
    """)

    # commit to database
    conn.commit()

    cur.close()
    conn.close()