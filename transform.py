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

    # Select only required columns and rename them
    df = df[list(mapping.keys())]
    df.rename(columns=mapping, inplace=True)

    # Data Cleaning: Handle missing values in the city column
    df['city'] = df['city'].fillna('Israel')

    # Basic string cleaning
    df['job_title'] = df['job_title'].str.strip()

    print(f"Transformation complete: Processed {len(df)} professional records.")
    return df