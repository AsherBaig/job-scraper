import json
import pandas as pd
from datetime import datetime, timedelta
from scraper.adzuna import fetch_jobs as adzuna_fetch
from scraper.berlinstartup import fetch_jobs as remotive_fetch


def filter_by_days(jobs, days=7):
    """Sirf last X days ki jobs rakho."""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []
    for job in jobs:
        date_str = job.get("posted_date", "")
        if not date_str:
            filtered.append(job)  # date nahi hai to rakho
            continue
        try:
            # Adzuna format: "2026-10-20T10:30:00Z"
            posted = datetime.strptime(date_str[:10], "%Y-%m-%d")
            if posted >= cutoff:
                filtered.append(job)
        except Exception:
            filtered.append(job)
    return filtered


def remove_duplicates(jobs):
    """Same URL wali jobs remove karo."""
    seen = set()
    unique = []
    for job in jobs:
        if job["url"] not in seen:
            seen.add(job["url"])
            unique.append(job)
    return unique


def save_csv(jobs, filepath="output/jobs.csv"):
    df = pd.DataFrame(jobs)
    df.to_csv(filepath, index=False, encoding="utf-8")
    print(f"Saved {len(jobs)} jobs → {filepath}")


def save_json(jobs, filepath="output/jobs.json"):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(jobs)} jobs → {filepath}")


def run():
    print("=" * 50)
    print(f"Job Scraper started at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    all_jobs = []

    # --- Source 1: Adzuna – Werkstudent in big cities ---
    for city in ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Bielefeld"]:
        all_jobs += adzuna_fetch("Werkstudent Software", city, 20)
        all_jobs += adzuna_fetch("Werkstudent Python", city, 20)
        all_jobs += adzuna_fetch("Werkstudent Full Stack", city, 20)

    # --- General roles ---
    all_jobs += adzuna_fetch("Full Stack Developer", "Berlin", 20)
    all_jobs += adzuna_fetch("Backend Engineer", "Munich", 20)
    all_jobs += adzuna_fetch("Software Engineer", "Munich", 20)

    # --- Source 2: Remotive – Remote English jobs ---
    all_jobs += remotive_fetch("software-dev", 20)
    all_jobs += remotive_fetch("data", 20)
    all_jobs += remotive_fetch("ai-ml-data-science", 20)

    # Duplicates remove karo
    unique_jobs = remove_duplicates(all_jobs)

    # Last 7 days ki jobs filter karo
    filtered_jobs = filter_by_days(unique_jobs, days=7)

    print(f"\nTotal unique jobs: {len(unique_jobs)}")
    print(f"Last 7 days jobs: {len(filtered_jobs)}")
    print("=" * 50)

    # Save karo
    save_csv(filtered_jobs)
    save_json(filtered_jobs)

    print("\nDone! Check output/ folder.")


if __name__ == "__main__":
    run()
