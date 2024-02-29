import psycopg2
from psycopg2 import sql
import json

import alpaca_trade_api as api
import pandas as pd
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()


# Logging of all closed orders (from server-side)
# This contains a lot more crucial information that cannot be obtained from client-side. (e.g. average filled price)
def log_closed_orders():
    alpaca = api.REST(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), "https://paper-api.alpaca.markets")
    all_closed_orders = alpaca.list_orders(status="closed", limit=500)
    all_orders_df = pd.DataFrame([order._raw for order in all_closed_orders])

    table_name = 'alpaca_closed_logs'

    # Create SQLAlchemy engine
    engine = create_engine(f'postgresql+psycopg2://postgres:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/postgres')

    # Upload DataFrame to PostgreSQL
    all_orders_df.to_sql(table_name, engine, index=False, if_exists='replace')  # Replace 'replace' with 'append' to add to an existing table instead of replacing it
    print(f'DataFrame uploaded to {table_name} successfully!')

# log_closed_orders()


# Logging of quantity, side, type, time in force, order class, stop loss and take profit to "trade_logs" table
def log_trade(symbol, qty, side, type, time_in_force, order_class, stop_loss, take_profit, news_trade_id, symbol_price, take_profit_pct, stop_loss_pct, position_per_trade, additional_info=None):
    try:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password=os.getenv("POSTGRES_PASSWORD"), port=5432)

        # Connect to your database
        cur = conn.cursor()

        # Create table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS trade_logs (
            trade_id SERIAL PRIMARY KEY,
            news_trade_id VARCHAR(40),
            trade_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            symbol VARCHAR(10),        
            side VARCHAR(5),
            type VARCHAR(20),
            time_in_force VARCHAR(20),
            order_class VARCHAR(20),
            symbol_price FLOAT,
            qty INT,
            stop_loss JSON,
            take_profit JSON,
            stop_loss_pct FLOAT,
            take_profit_pct FLOAT,
            position_per_trade FLOAT,
            additional_info JSONB
        );
        """)

        # Prepare the INSERT statement
        query = sql.SQL("""
        INSERT INTO trade_logs (trade_timestamp, symbol, qty, side, type, time_in_force, order_class, stop_loss, take_profit, news_trade_id, symbol_price, take_profit_pct, stop_loss_pct, position_per_trade, additional_info)
        VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
        
        # Convert python object to JSON string if it's not None
        stop_loss_json = json.dumps(stop_loss) if stop_loss is not None else None
        take_profit_json = json.dumps(take_profit) if take_profit is not None else None
        additional_info_json = json.dumps(additional_info) if additional_info is not None else None

        # Execute the INSERT statement
        cur.execute(query, (symbol, qty, side, type, time_in_force, order_class, stop_loss_json, take_profit_json, news_trade_id, symbol_price, take_profit_pct, stop_loss_pct, position_per_trade, additional_info_json))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Failed to log error to database: {e}")
        # Handle failure to log to database (e.g., fallback to logging to a file)


# Logging of news headline and impact score to "news_logs" table
def log_news(sym, headline, impact_buy, impact_sell, impact, news_trade_id, additional_info=None):
    try:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password=os.getenv("POSTGRES_PASSWORD"), port=5432)

        # Connect to your database
        cur = conn.cursor()

        # Create table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS news_logs (
            news_id SERIAL PRIMARY KEY,
            news_trade_id VARCHAR(40),
            news_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            sym VARCHAR(10),
            headline VARCHAR(500),
            impact_buy INT,
            impact_sell INT,
            impact INT,
            additional_info JSONB
        );
        """)

        # Prepare the INSERT statement
        query = sql.SQL("""
        INSERT INTO news_logs (news_timestamp, sym, headline, impact_buy, impact_sell, impact, news_trade_id, additional_info)
        VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s)
        """)
        
        # Convert additional_info to JSON string if it's not None
        additional_info_json = json.dumps(additional_info) if additional_info is not None else None

        # Execute the INSERT statement
        cur.execute(query, (sym, headline, impact_buy, impact_sell, impact, news_trade_id, additional_info_json))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Failed to log error to database: {e}")
        # Handle failure to log to database (e.g., fallback to logging to a file)


# Logging of news headline and impact score to "news_logs" table
def log_news_only(sym, headline, impact, additional_info=None):
    try:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password=os.getenv("POSTGRES_PASSWORD"), port=5432)

        # Connect to your database
        cur = conn.cursor()

        # Create table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS news_only_logs (
            news_id SERIAL PRIMARY KEY,
            news_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            sym VARCHAR(10),
            headline VARCHAR(500),
            impact INT,
            additional_info JSONB
        );
        """)

        # Prepare the INSERT statement
        query = sql.SQL("""
        INSERT INTO news_only_logs (news_timestamp, sym, headline, impact, additional_info)
        VALUES (NOW(), %s, %s, %s, %s)
        """)
        
        # Convert additional_info to JSON string if it's not None
        additional_info_json = json.dumps(additional_info) if additional_info is not None else None

        # Execute the INSERT statement
        cur.execute(query, (sym, headline, impact, additional_info_json))
        
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
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password=os.getenv("POSTGRES_PASSWORD"), port=5432)

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
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password=os.getenv("POSTGRES_PASSWORD"), port=5432)

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