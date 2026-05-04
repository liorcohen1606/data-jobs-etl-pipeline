import pandas as pd

def transform_job_data(raw_data):
    """
    Processes raw JSON data into a cleaned Pandas DataFrame.
    """
    if not raw_data:
        print("No data received for transformation.")
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)

    # Filter - Only jobs located in Israel (done before mapping)
    if 'job_country' in df.columns:
        df = df[df['job_country'] == 'IL']

    # Dictionary mapping JSearch fields to internal schema
    mapping = {
        'job_id': 'id',
        'job_title': 'job_title',
        'employer_name': 'company',
        'job_description': 'description',
        'job_city': 'city',
        'job_apply_link': 'apply_link'
    }

    # Column selection and renaming
    # Using only existing columns from the mapping to prevent KeyErrors
    existing_map_keys = [k for k in mapping.keys() if k in df.columns]
    df = df[existing_map_keys]
    df.rename(columns=mapping, inplace=True)

    # Text Processing - Shorten job description for better CSV readability
    if 'description' in df.columns:
        df['description'] = df['description'].apply(
            lambda x: (str(x)[:200] + '...') if len(str(x)) > 200 else str(x)
        )

    # Removing duplicate postings based on job title and company name
    initial_count = len(df)
    df.drop_duplicates(subset=['job_title', 'company'], keep='first', inplace=True)
    
    # Handling missing values
    if 'city' in df.columns:
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
