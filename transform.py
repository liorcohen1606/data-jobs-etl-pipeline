import pandas as pd

def transform_job_data(raw_data):
    """
    Processes raw JSON data into a cleaned Pandas DataFrame.
    """
    if not raw_data:
        print("No data received for transformation.")
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)
    
    # --- DEBUGGING PRINTS ---
    print(f"DEBUG: Total columns received: {df.columns.tolist()}")
    if not df.empty:
        # Checking potential location columns
        for col in ['job_country', 'job_location', 'job_country_name']:
            if col in df.columns:
                print(f"DEBUG: Column '{col}' sample values: {df[col].head(3).tolist()}")
    # -------------------------

    # 1. Flexible Filter - Looking for 'Israel' in any relevant location column
    # We check job_country first, then job_location as a backup
    is_israel = pd.Series(False, index=df.index)
    for col in ['job_country', 'job_location', 'job_country_name']:
        if col in df.columns:
            is_israel = is_israel | df[col].astype(str).str.contains('Israel', case=False, na=False)
    
    if is_israel.any():
        df = df[is_israel]
    else:
        print("WARNING: No records matched 'Israel'. Check debug prints for actual values.")

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
    existing_map_keys = [k for k in mapping.keys() if k in df.columns]
    df = df[existing_map_keys].copy()
    df.rename(columns=mapping, inplace=True)

    # 2. Text Processing - Shorten job description
    if 'description' in df.columns:
        df['description'] = df['description'].apply(
            lambda x: (str(x)[:200] + '...') if len(str(x)) > 200 else str(x)
        )

    # Set initial_count after filtering to see what we are working with
    initial_count = len(df)

    # Removing duplicate postings
    if not df.empty:
        df.drop_duplicates(subset=['job_title', 'company'], keep='first', inplace=True)
    
    # Handling missing values
    if 'city' in df.columns:
        df['city'] = df['city'].fillna('Israel')
    
    if not df.empty:
        df.dropna(subset=['job_title', 'company'], inplace=True)

    # Text cleaning
    if 'job_title' in df.columns:
        df['job_title'] = df['job_title'].str.strip()
    if 'company' in df.columns:
        df['company'] = df['company'].str.strip()

    # Type casting
    if 'description' in df.columns:
        df['description'] = df['description'].astype(str)

    print(f"Transformation complete: Processed {len(df)} records (Initial count after filtering: {initial_count}).")
    
    return df
