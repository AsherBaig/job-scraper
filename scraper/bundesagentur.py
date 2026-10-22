import requests
import pandas as pd
import json
from datetime import datetime

# Bundesagentur fuer Arbeit - Official German Job API (Free, No API key needed)
BASE_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"

# Request headers - required by the API
HEADERS = {
    "X-API-Key": "jobboerse-jobsuche",
    "Accept": "application/json",
}


def fetch_jobs(keywords="Software Engineer", location="", job_type=None, max_results=50):
    """
    Bundesagentur API se jobs fetch karta hai.

    keywords: job title ya skill (e.g. "Python Developer", "Werkstudent Software")
    location: city (e.g. "Berlin", "München", "Hamburg")
    job_type: "PART_TIME" for Werkstudent, "FULL_TIME" for fulltime, None for all
    max_results: kitne jobs chahiye
    """

    params = {
        "was": keywords,       # was = what (job title/keywords)
        "wo": location,        # wo = where (city)
        "size": max_results,
        "page": 1,
    }

    if job_type:
        params["arbeitszeit"] = job_type

    print(f"Fetching jobs: '{keywords}' in '{location or 'Germany'}'...")

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    data = response.json()
    jobs_raw = data.get("stellenangebote", [])

    print(f"Found {len(jobs_raw)} jobs")

    jobs = []
    for job in jobs_raw:
        jobs.append({
            "title": job.get("titel", ""),
            "company": job.get("arbeitgeber", ""),
            "location": job.get("arbeitsort", {}).get("ort", ""),
            "job_type": job.get("arbeitszeitModelle", []),
            "posted_date": job.get("eintrittsdatum", ""),
            "url": f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{job.get('hashId', '')}",
            "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    return jobs


def save_to_csv(jobs, filename="output/jobs.csv"):
    """Jobs ko CSV file mein save karta hai."""
    if not jobs:
        print("No jobs to save.")
        return

    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Saved {len(jobs)} jobs to {filename}")


def save_to_json(jobs, filename="output/jobs.json"):
    """Jobs ko JSON file mein save karta hai."""
    if not jobs:
        print("No jobs to save.")
        return

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(jobs)} jobs to {filename}")


if __name__ == "__main__":
    # --- Search 1: Werkstudent Software roles (English friendly) ---
    werkstudent_jobs = fetch_jobs(
        keywords="Werkstudent Software",
        location="",          # all of Germany
        job_type="PART_TIME",
        max_results=30,
    )

    # --- Search 2: Python Developer roles ---
    python_jobs = fetch_jobs(
        keywords="Python Developer",
        location="Berlin",
        max_results=20,
    )

    # --- Search 3: Full Stack roles ---
    fullstack_jobs = fetch_jobs(
        keywords="Full Stack Developer",
        location="",
        max_results=20,
    )

    # Sab results combine karo
    all_jobs = werkstudent_jobs + python_jobs + fullstack_jobs

    # Duplicates remove karo (same URL)
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        if job["url"] not in seen:
            seen.add(job["url"])
            unique_jobs.append(job)

    print(f"\nTotal unique jobs found: {len(unique_jobs)}")

    # Save karo
    save_to_csv(unique_jobs)
    save_to_json(unique_jobs)
