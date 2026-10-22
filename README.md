# Job Scraper – Automatisierte Datenextraktion

An automated job scraping solution built with Python, BeautifulSoup, and FastAPI that extracts job listings from multiple sources, filters them, and transforms the data into structured JSON/CSV datasets.

## Features

- Fetches jobs from multiple sources (Adzuna API, Remotive API)
- Filters by keywords, location, and job type
- Exports structured data to CSV and JSON
- Modular architecture – each source has its own scraper module

## Tech Stack

- **Python** – core language
- **requests** – HTTP calls to APIs and websites
- **BeautifulSoup** – HTML parsing and data extraction
- **pandas** – data transformation and CSV export
- **FastAPI** – REST API layer *(coming soon)*

## Project Structure

```
job-scraper/
├── scraper/
│   ├── adzuna.py        # Adzuna API – Germany jobs
│   ├── berlinstartup.py # Remotive API – Remote English jobs
│   └── runner.py        # Main entry point – runs all scrapers
├── output/
│   ├── jobs.csv         # Extracted job data
│   └── jobs.json        # Extracted job data (JSON)
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python3 -m scraper.runner
```

Results are saved to `output/jobs.csv` and `output/jobs.json`.

## Roadmap

- [ ] GitHub Actions – daily automated runs
- [ ] Email notifications for new jobs
- [ ] FastAPI REST endpoint
- [ ] Google Sheets integration
- [ ] Playwright for JavaScript-heavy sites (SAP, Siemens)
