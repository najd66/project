from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime
import uuid

router = APIRouter(
    prefix="/reporting",
    tags=["Reporting & Analytics"],
    responses={404: {"description": "Not found"}},
)

# Placeholder for report data
reports_db: Dict[str, Dict[str, Any]] = {}

class ReportGenerationRequest(BaseModel):
    report_name: str
    report_type: str # e.g., "comprehensive_security_assessment", "vulnerability_summary", "easm_findings"
    data_sources: List[str] # e.g., ["easm_results_id_123", "bas_simulation_id_456", "vulnerability_scan_id_789"]
    output_format: str = "pdf" # or "html", "json"
    # Parameters for LLMReportGenerator can be included here
    llm_params: Dict[str, Any] | None = None

class ReportStatus(BaseModel):
    report_id: str
    report_name: str
    report_type: str
    status: str # e.g., "pending", "generating", "completed", "failed"
    output_format: str
    download_url: str | None = None
    created_at: datetime.datetime
    completed_at: datetime.datetime | None = None

async def generate_report_background(report_id: str, request_details: ReportGenerationRequest):
    """Simulates background report generation."""
    print(f"Background task started for report_id: {report_id}")
    # Simulate time-consuming report generation
    import asyncio
    await asyncio.sleep(10) # Simulate 10 seconds of work
    
    # Update report status to completed (mock)
    if report_id in reports_db:
        reports_db[report_id]["status"] = "completed"
        reports_db[report_id]["completed_at"] = datetime.datetime.now()
        reports_db[report_id]["download_url"] = f"/reports/download/{report_id}/mock_report.{request_details.output_format}"
        print(f"Background task completed for report_id: {report_id}")
    else:
        print(f"Report ID {report_id} not found after background task completion.")

@router.post("/generate", response_model=ReportStatus, status_code=202, summary="Generate a New Security Report")
async def generate_new_report(request_details: ReportGenerationRequest, background_tasks: BackgroundTasks):
    """
    Submits a request to generate a new security report.

    - **report_name**: A user-defined name for the report.
    - **report_type**: Type of report to generate.
    - **data_sources**: List of IDs or references to data to be included in the report.
    - **output_format**: Desired output format (pdf, html, json).
    - **llm_params**: (Optional) Parameters for the LLM-based report generator.
    """
    report_id = "report_" + str(uuid.uuid4())
    current_time = datetime.datetime.now()
    
    new_report_status = ReportStatus(
        report_id=report_id,
        report_name=request_details.report_name,
        report_type=request_details.report_type,
        status="pending", # Will be updated by background task
        output_format=request_details.output_format,
        created_at=current_time
    )
    reports_db[report_id] = new_report_status.dict()

    # Trigger background task for report generation
    # In a real system, this would call the LLMReportGenerator module
    background_tasks.add_task(generate_report_background, report_id, request_details)
    
    print(f"Report generation task {report_id} ({request_details.report_name}) submitted.")
    return new_report_status

@router.get("/{report_id}", response_model=ReportStatus, summary="Get Report Status and Details")
async def get_report_status(report_id: str):
    """
    Retrieves the status and details of a specific report generation task.
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    return reports_db[report_id]

@router.get("/", response_model=List[ReportStatus], summary="List All Generated Reports")
async def list_all_reports():
    """
    Retrieves a list of all generated reports and their current status.
    """
    return list(reports_db.values())

# A mock download endpoint
@router.get("/download/{report_id}/{filename}", summary="Download Generated Report (Mock)")
async def download_report_mock(report_id: str, filename: str):
    if report_id not in reports_db or reports_db[report_id]["status"] != "completed":
        raise HTTPException(status_code=404, detail="Report not ready or not found")
    # In a real system, this would serve the actual file.
    # For now, just return a success message.
    return {"message": f"Mock download for report {report_id}, file {filename}. In a real system, this would be a file stream."}

