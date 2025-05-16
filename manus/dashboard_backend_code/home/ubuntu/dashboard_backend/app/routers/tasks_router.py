from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

router = APIRouter(
    prefix="/tasks",
    tags=["Task Management"],
    responses={404: {"description": "Not found"}},
)

# In-memory store for tasks (for demonstration purposes)
# In a real application, this would be a database or a more persistent store
tasks_db = {}

class TaskCreate(BaseModel):
    task_name: str
    module_to_run: str # e.g., "vulnerability_scan", "easm_discovery"
    target: str | None = None # e.g., a URL, IP range, or domain
    parameters: dict | None = None # Module-specific parameters

class TaskStatus(BaseModel):
    task_id: str
    task_name: str
    status: str # e.g., "pending", "running", "completed", "failed"
    module_to_run: str
    target: str | None = None
    submitted_at: str
    started_at: str | None = None
    completed_at: str | None = None
    result_summary: str | None = None

@router.post("/", response_model=TaskStatus, status_code=202, summary="Submit a New Security Task")
async def submit_new_task(task_details: TaskCreate):
    """
    Submits a new security task to the system.

    - **task_name**: A user-defined name for the task.
    - **module_to_run**: Identifier of the security module to execute (e.g., from advanced_security_script).
    - **target**: (Optional) The target for the security task.
    - **parameters**: (Optional) Additional parameters for the module.
    """
    task_id = str(uuid.uuid4())
    current_time = str(uuid.uuid4()) # Placeholder for actual timestamp
    new_task = TaskStatus(
        task_id=task_id,
        task_name=task_details.task_name,
        status="pending",
        module_to_run=task_details.module_to_run,
        target=task_details.target,
        submitted_at=current_time # Replace with actual datetime
    )
    tasks_db[task_id] = new_task.dict()
    
    # Here, you would typically trigger the WorkflowOrchestrator from advanced_security_script
    # to actually start processing this task asynchronously.
    # For now, we'll just simulate it as pending.
    print(f"Task {task_id} ({task_details.task_name}) submitted for module {task_details.module_to_run}.")
    
    return new_task

@router.get("/{task_id}", response_model=TaskStatus, summary="Get Task Status and Details")
async def get_task_status(task_id: str):
    """
    Retrieves the status and details of a specific security task.
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@router.get("/", response_model=list[TaskStatus], summary="List All Submitted Tasks")
async def list_all_tasks():
    """
    Retrieves a list of all submitted security tasks and their current status.
    """
    return list(tasks_db.values())

# Further endpoints could include:
# - PUT /tasks/{task_id}/cancel - To cancel a running task
# - GET /tasks/{task_id}/results - To get detailed results of a completed task
# - GET /tasks/{task_id}/logs - To stream logs for a task

