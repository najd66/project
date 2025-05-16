from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Assuming ConfigManager is accessible, e.g., from advanced_security_script.core.config_manager
# from advanced_security_script.core.config_manager import ConfigManager
# For now, we will simulate its behavior.

router = APIRouter(
    prefix="/config",
    tags=["System Configuration"],
    responses={404: {"description": "Not found"}, 403: {"description": "Operation not permitted"}},
)

# Simulated config store
# In a real scenario, ConfigManager would load from YAML files and manage this.
simulated_config_db: Dict[str, Any] = {
    "global": {
        "log_level": "INFO",
        "log_file_path": "/home/ubuntu/dashboard_backend/logs/system.log",
        "json_log_format": True
    },
    "llm_report_generator": {
        "model_name": "gpt-4-turbo-preview",
        "api_key_env": "OPENAI_API_KEY",
        "knowledge_base_path": "/home/ubuntu/dashboard_backend/advanced_security_script/data/knowledge_base"
    },
    "vulnerability_crawler": {
        "sources": ["NVD", "Exploit-DB"],
        "max_results_per_source": 50
    }
}

class ConfigUpdateRequest(BaseModel):
    module_name: str # e.g., "global", "llm_report_generator"
    config_key: str
    new_value: Any

@router.get("/", response_model=Dict[str, Any], summary="Get Full System Configuration")
async def get_full_configuration():
    """
    Retrieves the entire current system configuration.
    Sensitive values (like API keys) should ideally be masked or omitted in a real system.
    """
    # Real implementation: return ConfigManager.get_all_configs()
    return simulated_config_db

@router.get("/{module_name}", response_model=Dict[str, Any], summary="Get Module-Specific Configuration")
async def get_module_configuration(module_name: str):
    """
    Retrieves the configuration for a specific module.
    """
    # Real implementation: return ConfigManager.get_module_config(module_name)
    if module_name not in simulated_config_db:
        raise HTTPException(status_code=404, detail=f"Configuration for module 	{module_name}	 not found.")
    return simulated_config_db[module_name]

@router.put("/", response_model=Dict[str, Any], summary="Update System Configuration (Restricted)")
async def update_system_configuration(update_request: ConfigUpdateRequest):
    """
    Updates a specific configuration key for a module.
    This endpoint should be heavily restricted and require high privileges.

    - **module_name**: The name of the module configuration to update.
    - **config_key**: The specific key within the module's configuration.
    - **new_value**: The new value for the configuration key.
    """
    # Real implementation: ConfigManager.update_config(module_name, config_key, new_value) and save
    if update_request.module_name not in simulated_config_db:
        raise HTTPException(status_code=404, detail=f"Module 	{update_request.module_name}	 not found in configuration.")
    if update_request.config_key not in simulated_config_db[update_request.module_name]:
        raise HTTPException(status_code=404, detail=f"Key 	{update_request.config_key}	 not found in module 	{update_request.module_name}	 configuration.")
    
    simulated_config_db[update_request.module_name][update_request.config_key] = update_request.new_value
    print(f"Configuration updated: {update_request.module_name}.{update_request.config_key} = {update_request.new_value}")
    
    # Potentially trigger a reload of configurations in relevant modules
    return {"message": "Configuration updated successfully.", "updated_config": simulated_config_db[update_request.module_name]}

# Note: Actual saving of config changes to YAML files by ConfigManager is not simulated here.

