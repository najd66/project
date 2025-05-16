document.addEventListener("DOMContentLoaded", () => {
    const navButtons = document.querySelectorAll("nav button");
    const sections = document.querySelectorAll(".dashboard-section");
    const healthStatusDiv = document.getElementById("health-status");
    const tasksListDiv = document.getElementById("tasks-list");
    const newTaskForm = document.getElementById("new-task-form");
    const vulnerabilitiesListDiv = document.getElementById("vulnerabilities-list");
    const easmAssetsListDiv = document.getElementById("easm-assets-list");
    const basSimulationsListDiv = document.getElementById("bas-simulations-list");
    const reportsListDiv = document.getElementById("reports-list");
    const aiSecurityStatusDiv = document.getElementById("ai-security-status");
    const systemConfigDiv = document.getElementById("system-config");

    const API_BASE_URL = "https://api.shadow-evil.shop"; // Adjust if your API is elsewhere

    // --- Navigation --- 
    navButtons.forEach(button => {
        button.addEventListener("click", () => {
            const sectionId = button.getAttribute("data-section") + "-section";
            sections.forEach(section => {
                if (section.id === sectionId) {
                    section.classList.add("active-section");
                } else {
                    section.classList.remove("active-section");
                }
            });
            // Load content for the activated section
            loadSectionContent(button.getAttribute("data-section"));
        });
    });

    // --- API Fetch Utility ---
    async function fetchData(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error fetching ${endpoint}:`, error);
            return null;
        }
    }

    async function postData(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error posting to ${endpoint}:`, error);
            alert(`Error: ${error.message}`); // Show error to user
            return null;
        }
    }

    // --- Section Content Loaders ---
    async function loadHealthStatus() {
        const data = await fetchData("/health");
        if (data && healthStatusDiv) {
            healthStatusDiv.textContent = data.status || "Failed to load health status.";
        } else if (healthStatusDiv) {
            healthStatusDiv.textContent = "Failed to load health status.";
        }
    }

    async function loadTasks() {
        const data = await fetchData("/tasks/");
        if (data && tasksListDiv) {
            tasksListDiv.innerHTML = "<h3>Submitted Tasks:</h3>";
            if (data.length === 0) {
                tasksListDiv.innerHTML += "<p>No tasks submitted yet.</p>";
                return;
            }
            const ul = document.createElement("ul");
            ul.className = "item-list";
            data.forEach(task => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>ID:</strong> ${task.task_id} <br><strong>Name:</strong> ${task.task_name} <br><strong>Module:</strong> ${task.module_to_run} <br><strong>Status:</strong> ${task.status} <br><strong>Target:</strong> ${task.target || 'N/A'}`;
                ul.appendChild(li);
            });
            tasksListDiv.appendChild(ul);
        } else if (tasksListDiv) {
            tasksListDiv.innerHTML = "<p>Failed to load tasks.</p>";
        }
    }

    async function loadVulnerabilities() {
        const data = await fetchData("/intelligence/vulnerabilities?limit=5");
        if (data && vulnerabilitiesListDiv) {
            vulnerabilitiesListDiv.innerHTML = "<h3>Latest Vulnerabilities:</h3>";
             if (data.length === 0) {
                vulnerabilitiesListDiv.innerHTML += "<p>No vulnerabilities found.</p>";
                return;
            }
            const ul = document.createElement("ul");
            ul.className = "item-list";
            data.forEach(vuln => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>ID:</strong> ${vuln.id} <br><strong>Title:</strong> ${vuln.title} <br><strong>Source:</strong> ${vuln.source} <br><strong>Severity:</strong> ${vuln.severity || 'N/A'}`;
                ul.appendChild(li);
            });
            vulnerabilitiesListDiv.appendChild(ul);
        } else if (vulnerabilitiesListDiv) {
            vulnerabilitiesListDiv.innerHTML = "<p>Failed to load vulnerabilities.</p>";
        }
    }
    
    async function loadEASMAssets() {
        const data = await fetchData("/easm/assets?limit=5");
        if (data && easmAssetsListDiv) {
            easmAssetsListDiv.innerHTML = "<h3>Discovered EASM Assets:</h3>";
            if (data.length === 0) {
                easmAssetsListDiv.innerHTML += "<p>No EASM assets found.</p>";
                return;
            }
            const ul = document.createElement("ul");
            ul.className = "item-list";
            data.forEach(asset => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>ID:</strong> ${asset.id} <br><strong>Type:</strong> ${asset.asset_type} <br><strong>Identifier:</strong> ${asset.identifier} <br><strong>Risk:</strong> ${asset.risk_score || 'N/A'}`;
                ul.appendChild(li);
            });
            easmAssetsListDiv.appendChild(ul);
        } else if (easmAssetsListDiv) {
            easmAssetsListDiv.innerHTML = "<p>Failed to load EASM assets.</p>";
        }
    }

    async function loadBASSimulations() {
        const data = await fetchData("/bas/simulations");
        if (data && basSimulationsListDiv) {
            basSimulationsListDiv.innerHTML = "<h3>BAS Simulations:</h3>";
            if (data.length === 0) {
                basSimulationsListDiv.innerHTML += "<p>No BAS simulations found.</p>";
                return;
            }
            const ul = document.createElement("ul");
            ul.className = "item-list";
            data.forEach(sim => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>ID:</strong> ${sim.simulation_id} <br><strong>Name:</strong> ${sim.simulation_name} <br><strong>Status:</strong> ${sim.status}`;
                ul.appendChild(li);
            });
            basSimulationsListDiv.appendChild(ul);
        } else if (basSimulationsListDiv) {
            basSimulationsListDiv.innerHTML = "<p>Failed to load BAS simulations.</p>";
        }
    }

    async function loadReports() {
        const data = await fetchData("/reporting/");
        if (data && reportsListDiv) {
            reportsListDiv.innerHTML = "<h3>Generated Reports:</h3>";
            if (data.length === 0) {
                reportsListDiv.innerHTML += "<p>No reports found.</p>";
                return;
            }
            const ul = document.createElement("ul");
            ul.className = "item-list";
            data.forEach(report => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>ID:</strong> ${report.report_id} <br><strong>Name:</strong> ${report.report_name} <br><strong>Status:</strong> ${report.status} <br>${report.download_url ? `<a href="${API_BASE_URL}${report.download_url}" target="_blank">Download (Mock)</a>` : "Processing"}`;
                ul.appendChild(li);
            });
            reportsListDiv.appendChild(ul);
        } else if (reportsListDiv) {
            reportsListDiv.innerHTML = "<p>Failed to load reports.</p>";
        }
    }

    async function loadAIsecurityStatus() {
        // Example: Fetching metrics for a specific model
        const modelId = "example_model_v1"; 
        const data = await fetchData(`/ai-security/trustworthy-ai/metrics/${modelId}`);
        if (data && aiSecurityStatusDiv) {
            aiSecurityStatusDiv.innerHTML = `<h3>Trustworthy AI Metrics for ${data.model_id}:</h3>
                                           <p>Transparency: ${data.transparency_score || 'N/A'}</p>
                                           <p>Fairness: ${data.fairness_score || 'N/A'}</p>
                                           <p>Explainability: ${data.explainability_summary || 'N/A'}</p>
                                           <p>Last Assessed: ${new Date(data.last_assessment_date).toLocaleString()}</p>`;
        } else if (aiSecurityStatusDiv) {
            aiSecurityStatusDiv.innerHTML = "<p>Failed to load AI security status or model not found.</p>";
        }
    }

    async function loadSystemConfig() {
        const data = await fetchData("/config/");
        if (data && systemConfigDiv) {
            systemConfigDiv.innerHTML = "<h3>Current System Configuration:</h3><pre>" + JSON.stringify(data, null, 2) + "</pre>";
        } else if (systemConfigDiv) {
            systemConfigDiv.innerHTML = "<p>Failed to load system configuration.</p>";
        }
    }


    function loadSectionContent(sectionName) {
        switch (sectionName) {
            case "overview":
                loadHealthStatus();
                break;
            case "tasks":
                loadTasks();
                break;
            case "intelligence":
                loadVulnerabilities();
                break;
            case "easm":
                loadEASMAssets();
                break;
            case "bas":
                loadBASSimulations();
                break;
            case "reporting":
                loadReports();
                break;
            case "ai-security":
                loadAIsecurityStatus();
                break;
            case "config":
                loadSystemConfig();
                break;
        }
    }

    // --- Form Submissions ---
    if (newTaskForm) {
        newTaskForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const formData = new FormData(newTaskForm);
            const taskDetails = {
                task_name: formData.get("task_name"),
                module_to_run: formData.get("module_to_run"),
                target: formData.get("target") || null,
                // parameters: {} // Add if you have parameter inputs
            };
            const result = await postData("/tasks/", taskDetails);
            if (result) {
                alert(`Task ${result.task_id} submitted successfully! Status: ${result.status}`);
                newTaskForm.reset();
                loadTasks(); // Refresh the tasks list
            }
        });
    }

    // --- Initial Load ---
    loadHealthStatus(); // Load health status on page load for the default section

});

