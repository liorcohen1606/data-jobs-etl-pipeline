import requests
import pandas as pd

API_URL = "https://jsonplaceholder.typicode.com/posts"

def extract_job_data():
    """
    Fetches job listing data from the specified API URL.
    Returns the data as a list of dictionaries, or an empty list if it fails.
    """
    print("Starting data extraction...")

    try:
        # Send a GET request to the API
        response = requests.get(API_URL)
        # Check if the request was successful (HTTP Status code 200)
        response.raise_for_status()
        # Parse the response text into a JSON format
        data = response.json()
        print("Data extracted successfully!")
        return data
    except requests.exceptions.RequestException as e:
        # Handle any network errors or bad responses (Http status code 404 \ 500)
        print(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    # Execute the extraction function
    raw_data = extract_job_data()

    if raw_data:
        print(raw_data[0])
    



