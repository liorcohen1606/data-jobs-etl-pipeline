import pandas as pd

def transform_job_data(raw_data):
    """
    Processes raw JSON data into a cleaned Pandas DataFrame.
    """
    if not raw_data:
        print("No data received for transformation.")
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)

    # Flexible Israel Filter
    # Checking multiple columns for 'Israel' to ensure location accuracy
    is_israel = pd.Series(False, index=df.index)
    location_cols = ['job_country', 'job_location', 'job_country_name']
    
    for col in location_cols:
        if col in df.columns:
            is_israel = is_israel | df[col].astype(str).str.contains('Israel', case=False, na=False)
    
    df = df[is_israel].copy()

    # Schema Mapping
    mapping = {
        'job_id': 'id',
        'job_title': 'job_title',
        'employer_name': 'company',
        'job_description': 'description',
        'job_city': 'city',
        'job_apply_link': 'apply_link'
    }

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
        df.drop_duplicates(subset=['job_title', 'company'], keep='first', inplace=True)
        
        if 'city' in df.columns:
            df['city'] = df['city'].fillna('Israel')
            
        df.dropna(subset=['job_title', 'company'], inplace=True)
        
        # Cleanup strings
        for col in ['job_title', 'company']:
            if col in df.columns:
                df[col] = df[col].str.strip()

        removed = initial_count - len(df)
        print(f"Transformation complete: Processed {len(df)} records (Removed {removed} duplicates).")
    
    return df
