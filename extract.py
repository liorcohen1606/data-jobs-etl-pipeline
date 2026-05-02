import requests
import pandas as pd
from api_keys import RAPID_API_KEY
import os

try:
    from api_keys import RAPID_API_KEY
except ImportError:
    RAPID_API_KEY = os.getenv('RAPID_API_KEY')

def extract_job_data():
    """
    Fetches real-time tech jobs in Israel from JSearch 
    """
    url = "https://jsearch.p.rapidapi.com/search"
    
    
    headers = {
        "x-rapidapi-key":RAPID_API_KEY, 
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    # List of queries we want to search for
    search_queries = ["Data Student", "Software Student"]
    
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


