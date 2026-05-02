import pandas as pd
from extract import extract_job_data


def transform_job_data(raw_data):
    """
    Processes raw JSON data into a cleaned Pandas DataFrame.
    """
    if not raw_data:
        print("No data received for transformation.")
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)

    # Dictionary mapping JSearch fields to internal schema
    mapping = {
        'job_id': 'id',
        'job_title': 'job_title',
        'employer_name': 'company',
        'job_description': 'description',
        'job_city': 'city',
        'job_apply_link': 'apply_link'
    }

    #Column selection and renaming
    df = df[list(mapping.keys())]
    df.rename(columns=mapping, inplace=True)

    # Removing duplicate postings based on job title and company name
    initial_count = len(df)
    df.drop_duplicates(subset=['job_title', 'company'], keep='first', inplace=True)
    
    #Handling missing values
    df['city'] = df['city'].fillna('Israel')
    df.dropna(subset=['job_title', 'company'], inplace=True)

    # Text cleaning
    # Stripping whitespace from critical string columns
    df['job_title'] = df['job_title'].str.strip()
    df['company'] = df['company'].str.strip()

    # Type casting for future visualization
    # Ensuring description is string type for keyword searching
    df['description'] = df['description'].astype(str)

    removed = initial_count - len(df)
    print(f"Transformation complete: Processed {len(df)} records (Removed {removed} duplicates).")
    
    return df