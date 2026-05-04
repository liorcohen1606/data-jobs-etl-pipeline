import sqlite3
import pandas as pd

def load_data_to_sqlite(df, db_name="jobs_data.sqlite3", table_name="cleaned_jobs"):
    """
    Saves a Pandas DataFrame into an SQLite database.
    If the table exists, it appends new data.
    """

    if df.empty :
        print("No data to load")
        return
    
    print(f"Connecting to database: {db_name}...")
    # Create a connection to the SQLite database
    connect = sqlite3.connect(db_name)
    try:
        df.to_sql(table_name, connect, if_exists='replace', index=False)
        df.to_csv('all_jobs.csv', index=False, encoding='utf-8-sig')
        print(f"Success! Data loaded into table '{table_name}'.")

    except Exception as e:
        print(f"Error loading data to SQL: {e}")

    finally:
        connect.close()

if __name__ == "__main__":
    print("Running local test with dummy data...")
    # For a quick test, we can try to load some dummy data
    test_df = pd.DataFrame({
        'id': [1, 2],
        'job_title': ['test developer', 'data engineer'],
        'job_description': ['desc 1', 'desc 2']
    })
    load_data_to_sqlite(test_df)
