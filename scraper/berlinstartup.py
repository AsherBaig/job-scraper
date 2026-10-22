import requests
from bs4 import BeautifulSoup


def fetch_jobs(keywords="software", max_results=20):
    """
    Remotive.com API se remote English tech jobs fetch karta hai.
    BeautifulSoup se JSON response parse karta hai.

    keywords: job category (e.g. "software-dev", "devops-sysadmin", "data")
    """

    print(f"[Remotive] Fetching remote '{keywords}' jobs...")

    url = f"https://remotive.com/api/remote-jobs?category={keywords}&limit={max_results}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[Remotive] Error: {response.status_code}")
        return []

    # JSON response parse karo
    data = response.json()
    jobs_raw = data.get("jobs", [])

    print(f"[Remotive] Found {len(jobs_raw)} jobs")

    jobs = []
    for job in jobs_raw:
        jobs.append({
            "source": "Remotive",
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "location": job.get("candidate_required_location", "Worldwide"),
            "salary_min": "",
            "salary_max": job.get("salary", ""),
            "description": BeautifulSoup(job.get("description", ""), "html.parser").get_text()[:200],
            "url": job.get("url", ""),
            "posted_date": job.get("publication_date", ""),
        })

    return jobs
