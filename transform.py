import pandas as pd
from extract import extract_job_data

def transform_job_data(raw_data):

    """
    Transforms raw JSON data into a clean Pandas DataFrame.
    Filters columns, renames them, and standardizes text.
    """
    print("Starting data transformation...")

    if not raw_data:
        print("No data provided for transformation.")
        return pd.DataFrame()
    
    #Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(raw_data)
    #Keep only the necessary columns
    columns_to_keep = ['id','title', 'body'] 
    df = df[columns_to_keep]
    #Rename columns to match our job board context
    df.rename(columns={'body': 'job_description', 'title': 'job_title'}, inplace=True)
    #Clean data: Convert all job titles to lowercase for consistent searching
    df['job_description'] = df['job_description'].str.lower()
    print(f"Transformation complete! Processed {len(df)} rows.")
    return df

if __name__ == "__main__":
    # Fetch the raw data using the function from extract.py
    data = extract_job_data()
    
    # Process the raw data into a structured table
    cleaned_df = transform_job_data(data)
    
    # Display the first 5 rows of the cleaned data
    if not cleaned_df.empty:
        print("\nCleaned Data Preview (Top 5 rows):")
        print(cleaned_df.head())