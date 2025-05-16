from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Tambahkan import ini

# Impor router Anda seperti sebelumnya
from app.routers import (
    tasks_router, 
    intelligence_router, 
    easm_router, 
    bas_router, 
    reporting_router,
    ai_security_router,
    config_router
)

app = FastAPI(
    title="Shadow Evil Security Dashboard API",
    description="API for the Advanced Cybersecurity Monitoring and Operations Dashboard.",
    version="0.1.0",
    openapi_tags=[
        {"name": "System Status", "description": "API health and status."},
        {"name": "Task Management", "description": "Manage and monitor security tasks."},
        {"name": "Threat Intelligence", "description": "Access and manage threat intelligence data."},
        {"name": "External Attack Surface Management", "description": "Manage EASM operations and discovered assets."},
        {"name": "Breach and Attack Simulation", "description": "Launch and monitor BAS simulations."},
        {"name": "Reporting & Analytics", "description": "Generate and retrieve security reports."},
        {"name": "AI Security & Trustworthiness", "description": "Manage AI model security and trustworthiness assessments."},
        {"name": "System Configuration", "description": "Manage system-wide and module-specific configurations."}
    ]
)

# Tambahkan Middleware CORS
origins = [
    "http://shadow-evil.shop",    # Domain frontend Anda
    "https://shadow-evil.shop",   # Jika menggunakan HTTPS
    "http://localhost",           # Untuk pengujian lokal frontend
    "http://localhost:8080",      # Contoh port lokal frontend jika Anda menjalankannya seperti itu
    # Anda bisa menambahkan origin lain jika diperlukan
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Izinkan origin spesifik
    allow_credentials=True,
    allow_methods=["*"],         # Izinkan semua metode (GET, POST, dll. )
    allow_headers=["*"],         # Izinkan semua header
)


@app.get("/health", tags=["System Status"], summary="Health Check")
async def health_check():
    """
    Provides a simple health check endpoint to confirm the API is running.
    """
    return {"status": "API is healthy and running!"}

# Sertakan semua router
app.include_router(tasks_router.router)
app.include_router(intelligence_router.router)
app.include_router(easm_router.router)
app.include_router(bas_router.router)
app.include_router(reporting_router.router)
app.include_router(ai_security_router.router)
app.include_router(config_router.router)

# Contoh perintah untuk menjalankan dari /home/ajul/dashboard_backend:
# python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
