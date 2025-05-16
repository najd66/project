from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime

router = APIRouter(
    prefix="/intelligence",
    tags=["Threat Intelligence"],
    responses={404: {"description": "Not found"}},
)

# Placeholder for in-memory storage or database interaction
vulnerabilities_db: List[Dict[str, Any]] = []

class Vulnerability(BaseModel):
    id: str
    source: str # e.g., NVD, Exploit-DB
    title: str
    description: str
    severity: str | None = None # e.g., CRITICAL, HIGH, MEDIUM, LOW
    cvss_score: float | None = None
    references: List[str] | None = []
    published_date: datetime.datetime
    last_modified_date: datetime.datetime

@router.get("/vulnerabilities", response_model=List[Vulnerability], summary="Get Latest Vulnerabilities")
async def get_latest_vulnerabilities(limit: int = 10, source: str | None = None, severity: str | None = None):
    """
    Retrieves a list of the latest vulnerabilities, with optional filtering.

    - **limit**: Maximum number of vulnerabilities to return.
    - **source**: Filter by vulnerability source (e.g., "NVD").
    - **severity**: Filter by severity level (e.g., "CRITICAL").
    """
    # This is a placeholder. In a real implementation, this would query
    # the VulnerabilityCrawler module or a database populated by it.
    # Simulating some data for now:
    simulated_data = [
        {
            "id": "CVE-2025-0001",
            "source": "NVD",
            "title": "Example Critical Vulnerability in WebServerX",
            "description": "A remote code execution vulnerability exists in WebServerX due to improper input validation.",
            "severity": "CRITICAL",
            "cvss_score": 9.8,
            "references": ["http://nvd.nist.gov/vuln/detail/CVE-2025-0001"],
            "published_date": datetime.datetime.now() - datetime.timedelta(days=1),
            "last_modified_date": datetime.datetime.now()
        },
        {
            "id": "EDB-ID-2025-0002",
            "source": "Exploit-DB",
            "title": "WebServerY - SQL Injection PoC",
            "description": "Proof of concept for SQL injection in WebServerY login page.",
            "severity": "HIGH",
            "cvss_score": 7.5,
            "references": ["http://exploit-db.com/exploits/20250002"],
            "published_date": datetime.datetime.now() - datetime.timedelta(days=2),
            "last_modified_date": datetime.datetime.now() - datetime.timedelta(days=1)
        }
    ]
    
    results = simulated_data
    if source:
        results = [v for v in results if v["source"].lower() == source.lower()]
    if severity:
        results = [v for v in results if v["severity"].lower() == severity.lower()]
    
    return results[:limit]

@router.post("/vulnerabilities/crawl", status_code=202, summary="Trigger Vulnerability Crawling Task")
async def trigger_vulnerability_crawl(sources: List[str] | None = ["NVD", "Exploit-DB"]):
    """
    Triggers a new task to crawl for the latest vulnerabilities from specified sources.
    This would typically integrate with the tasks_router and the VulnerabilityCrawler module.
    """
    # In a real implementation, this would create a task via the tasks_router
    # and the WorkflowOrchestrator would invoke the VulnerabilityCrawler.
    task_id = "crawl_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print(f"Vulnerability crawl task {task_id} triggered for sources: {sources}")
    return {"message": "Vulnerability crawl task submitted.", "task_id": task_id}

# More endpoints can be added, e.g., for specific vulnerability details by ID, statistics, etc.

