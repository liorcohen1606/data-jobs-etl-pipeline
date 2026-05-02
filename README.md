# Student Tech Market ETL Pipeline

## Project Overview
This project implements an automated ETL pipeline designed to track job opportunities for students in the Israeli tech market. The system handles the entire data lifecycle: from fetching real-time listings via external APIs to processing and persistent storage in a local SQL database.

## Architecture & Workflow
The pipeline is modularly structured into three main stages:

1. **Extract**: Fetches real-time job data from multiple sources (LinkedIn, Indeed, Glassdoor) using the JSearch API. It supports multi-query execution to gather data for different roles (e.g., Data Student and Software Student) in a single run.
2. **Transform**: Processes raw JSON responses using Pandas. This stage includes data cleaning, handling missing values, and standardizing features like job titles and locations to ensure data quality.
3. **Load**: Persists the cleaned data into a local SQLite database, allowing for historical tracking and efficient querying.

## Tech Stack
* **Language**: Python 3.x
* **Data Processing**: Pandas
* **Database**: SQLite3
* **API Integration**: Requests (JSearch via RapidAPI)

## Key Technical Features
* **Multi-Query Support**: Aggregates data from diverse search terms into a unified dataset.
* **Localization**: Optimized for the Israeli market with specific geographic filtering.
* **Security**: Externalized API credentials using secret management to prevent exposure in version control.

## Getting Started
### Prerequisites
* Python 3.x
* Required libraries: `pip install pandas requests`

### Configuration
Create an `api_keys.py` file in the root directory and add your API key:
```python
RAPID_API_KEY = "your_api_key_here"