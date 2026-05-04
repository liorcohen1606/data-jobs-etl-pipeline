import requests
import pandas as pd
import os

def get_api_key():
    try:
        from api_keys import RAPID_API_KEY
        return RAPID_API_KEY
    except ImportError:
        return os.getenv('RAPID_API_KEY')
    
def extract_job_data():
    """
    Fetches real-time tech jobs in Israel from JSearch 
    """
    url = "https://jsearch.p.rapidapi.com/search"
    api_key = get_api_key()
    
    if not api_key:
        print("Error: RAPID_API_KEY not found.")
        return []
    
    
    headers = {
        "x-rapidapi-key":api_key, 
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    # List of queries we want to search for
    search_queries = [
        "Data Student", 
        "Software Student", 
        "DevOps Student"
    ]
    
    # This empty list will collect jobs from all queries
    all_extracted_jobs = []

    for query in search_queries:
        print(f"Fetching jobs for query: '{query}'...")
        
        querystring = {
            "query": query, 
            "country": "Israel",
            "num_pages": "1"
        }

        try:
            print("Connecting to JSearch API...")
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('data', []) # JSearch nests results under the 'data' key
            
            print(f"Found {len(jobs)} jobs for '{query}'.")
            # Add the jobs found in this iteration to our main list
            all_extracted_jobs.extend(jobs)

        except Exception as e:
            print(f"Extraction failed for '{query}': {e}")
            print(f"Total jobs extracted across all queries: {len(all_extracted_jobs)}")
    return all_extracted_jobs

if __name__ == "__main__":
    results = extract_job_data()


