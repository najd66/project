# advanced_security_script/tests/unit/test_workflow_orchestrator.py

import unittest
import os
import yaml
from advanced_security_script.core.workflow_orchestrator import WorkflowOrchestrator
# We will mock other managers and modules for this unit test

# Helper to create a temporary config file
def create_temp_config_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(content, f)

class TestWorkflowOrchestrator(unittest.TestCase):
    def setUp(self):
        self.test_configs_dir = "/home/ubuntu/advanced_security_script/tests/unit/temp_configs_orchestrator"
        os.makedirs(self.test_configs_dir, exist_ok=True)
        self.default_config_path = os.path.join(self.test_configs_dir, "default_orchestrator_config.yaml")

        self.default_config_content = {
            "global": {
                "log_level": "INFO",
                "log_file_path": "/home/ubuntu/advanced_security_script/tests/unit/temp_logs/orchestrator_unit_test.log",
                "json_log_format": False
            },
            "workflow_settings": {
                "default_timeout": 60
            }
        }
        create_temp_config_file(self.default_config_path, self.default_config_content)

        # Ensure log directory for orchestrator test exists
        os.makedirs(os.path.dirname(self.default_config_content["global"]["log_file_path"]), exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.default_config_path):
            os.remove(self.default_config_path)
        log_file = self.default_config_content["global"]["log_file_path"]
        if os.path.exists(log_file):
            os.remove(log_file)
        
        # Clean up directories if empty
        if os.path.exists(os.path.dirname(log_file)) and not os.listdir(os.path.dirname(log_file)):
            os.rmdir(os.path.dirname(log_file))
        if os.path.exists(self.test_configs_dir) and not os.listdir(self.test_configs_dir):
            os.rmdir(self.test_configs_dir)

    def test_orchestrator_initialization(self):
        orchestrator = WorkflowOrchestrator(config_path=self.default_config_path)
        self.assertIsNotNone(orchestrator.config_manager)
        self.assertIsNotNone(orchestrator.logger_manager)
        self.assertIsNotNone(orchestrator.logger)
        self.assertEqual(orchestrator.config_manager.get("workflow_settings", "default_timeout"), 60)
        self.orchestrator_logger = orchestrator.logger # Save for checking log output

    def test_run_test_setup_workflow(self):
        orchestrator = WorkflowOrchestrator(config_path=self.default_config_path)
        task_config = {"task_name": "test_setup"}
        result = orchestrator.run_workflow(task_config)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Test setup workflow executed.")

        # Check logs (basic check, more advanced log checking might require capturing logs)
        log_content = []
        log_file_path = orchestrator.config_manager.get("global", "log_file_path")
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as f:
                log_content = f.readlines()
        self.assertTrue(any("Executing 'test_setup' workflow." in line for line in log_content))

    def test_run_unknown_task_workflow(self):
        orchestrator = WorkflowOrchestrator(config_path=self.default_config_path)
        task_config = {"task_name": "non_existent_task_123"}
        result = orchestrator.run_workflow(task_config)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Unknown task: non_existent_task_123")

    def test_crawl_vulnerabilities_test_workflow_pending(self):
        """Tests the placeholder behavior for a module not yet fully integrated."""
        orchestrator = WorkflowOrchestrator(config_path=self.default_config_path)
        task_config = {"task_name": "crawl_vulnerabilities_test"}
        result = orchestrator.run_workflow(task_config)
        self.assertEqual(result["status"], "pending_integration")
        self.assertTrue("VulnerabilityCrawler test pending full integration" in result["message"])

    # Add more tests here as modules get integrated into the orchestrator:
    # - Mocking module dependencies (e.g., VulnerabilityCrawler, LLMReportGenerator)
    # - Testing data flow between mocked modules via the orchestrator
    # - Testing error handling when a module within the workflow fails

if __name__ == "__main__":
    unittest.main()

