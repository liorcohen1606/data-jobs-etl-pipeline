from extract import extract_job_data
from transform import transform_job_data
from load import load_data_to_sqlite

def run_pipeline():
    print("Starting ETL Pipeline")
    
    #EXTRACT
    raw_data = extract_job_data()
    
    #TRANSFORM
    cleaned_df = transform_job_data(raw_data)
    
    #LOAD
    load_data_to_sqlite(cleaned_df)
    
    print("Pipeline Finished Successfully")

if __name__ == "__main__":
    run_pipeline()