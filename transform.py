import pandas as pd

def transform_job_data(raw_data):
    """
    Processes raw JSON data into a cleaned Pandas DataFrame.
    No strict filtering to ensure data flow.
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
        'job_location': 'location',
        'job_apply_link': 'apply_link'
    }

    # Column selection and renaming
    existing_keys = [k for k in mapping.keys() if k in df.columns]
    df = df[existing_keys].copy()
    df.rename(columns=mapping, inplace=True)

    # Text Processing - Shorten description for readability
    if 'description' in df.columns:
        df['description'] = df['description'].apply(
            lambda x: (str(x)[:200] + '...') if len(str(x)) > 200 else str(x)
        )

    # Cleaning and Deduplication
    if not df.empty:
        initial_count = len(df)
        
        # Deduplicate to keep the file clean
        df.drop_duplicates(subset=['job_title', 'company'], keep='first', inplace=True)
        
        # Basic cleanup
        if 'city' in df.columns:
            df['city'] = df['city'].fillna('N/A')
            
        df.dropna(subset=['job_title', 'company'], inplace=True)
        
        # Cleanup strings
        for col in ['job_title', 'company']:
            if col in df.columns:
                df[col] = df[col].str.strip()

        print(f"Transformation complete: Processed {len(df)} records.")
    
    return df
