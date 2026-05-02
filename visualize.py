import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def generate_job_visualizations(db_path='jobs_data.sqlite3'):
    """
    Generates professional insights from the SQLite database.
    Focuses on Company distribution and Tech Stack.
    """
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM cleaned_jobs"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            print("Database is empty. Run the pipeline first.")
            return
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    sns.set_theme(style="whitegrid")


    #Visualization: Technology Demand
    tech_keywords = ['Python', 'SQL', 'C++', 'Java', 'AWS', 'Spark', 'R', 'Excel', 'Docker']
    tech_counts = {tech: 0 for tech in tech_keywords}
    df['description'] = df['description'].astype(str)
    
    for tech in tech_keywords:
        tech_counts[tech] = df['description'].str.contains(tech, case=False).sum()
        
    tech_series = pd.Series(tech_counts).sort_values(ascending=False)
    
    plt.figure(figsize=(10, 8))
    sns.barplot(x=tech_series.values, y=tech_series.index, palette='mako')
    plt.title('Tech Stack Demand for Student Roles', fontsize=15)
    plt.xlabel('Frequency in Descriptions', fontsize=12)
    plt.ylabel('Technology', fontsize=12)
    plt.tight_layout()
    plt.savefig('top_technologies.png')
    plt.close()
    print("Generated: top_technologies.png")

if __name__ == "__main__":
    generate_job_visualizations()