import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/de/search/1"


def fetch_jobs(keywords="Software Engineer", location="Berlin", max_results=20):
    """
    Adzuna API se Germany jobs fetch karta hai.

    keywords: job title ya skill (e.g. "Werkstudent Python", "Full Stack Developer")
    location: city (e.g. "Berlin", "Munich", "Hamburg")
    max_results: kitne jobs chahiye (max 50 per request)
    """

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": max_results,
        "what": keywords,       # job title / keywords
        "where": location,      # city / location
        "content-type": "application/json",
    }

    print(f"[Adzuna] Fetching: '{keywords}' in '{location}'...")

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"[Adzuna] Error: {response.status_code}")
        return []

    data = response.json()
    jobs_raw = data.get("results", [])

    print(f"[Adzuna] Found {len(jobs_raw)} jobs")

    # Sirf zaroori fields nikaalo - clean karo
    jobs = []
    for job in jobs_raw:
        jobs.append({
            "source": "Adzuna",
            "title": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", ""),
            "location": job.get("location", {}).get("display_name", ""),
            "salary_min": job.get("salary_min", ""),
            "salary_max": job.get("salary_max", ""),
            "description": job.get("description", "")[:200],  # first 200 chars
            "url": job.get("redirect_url", ""),
            "posted_date": job.get("created", ""),
        })

    return jobs
