import json
import pandas as pd
from datetime import datetime
from scraper.adzuna import fetch_jobs as adzuna_fetch
from scraper.berlinstartup import fetch_jobs as remotive_fetch


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

    # --- Source 1: Adzuna – Germany jobs ---
    all_jobs += adzuna_fetch("Werkstudent Software", "Berlin", 20)
    all_jobs += adzuna_fetch("Python Developer", "Germany", 20)
    all_jobs += adzuna_fetch("Full Stack Developer", "Berlin", 20)

    # --- Source 2: Remotive – Remote English jobs ---
    all_jobs += remotive_fetch("software-dev", 20)

    # Duplicates remove karo
    unique_jobs = remove_duplicates(all_jobs)

    print(f"\nTotal unique jobs: {len(unique_jobs)}")
    print("=" * 50)

    # Save karo
    save_csv(unique_jobs)
    save_json(unique_jobs)

    print("\nDone! Check output/ folder.")


if __name__ == "__main__":
    run()
