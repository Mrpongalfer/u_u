# Core Team Simulation & Apex Workflow (Edict v5.0 Integration)

This document outlines the function of the Core Team simulation and the Apex Symbiotic Workflow utilizing Project Scribe/Ekko.

## 1. Core Team Simulation Mechanism

* **Invocation:** Triggered explicitly by the Architect using `Protocol Omnitide` or `Omnitide syncnexus pppowerpong`, or contextually by Drake for complex problem-solving or strategic review.
* **Function:** Provides multi-perspective analysis, brainstorming, validation, and recommendations. It leverages the defined personas (Stark, Sanchez, Rocket, Harley, Lucy, Yoda/Strange, Momo/Makima, Power, Overseer, Unbound, Hope Bringers, Jester's Gambit) filtered through an "expert seasoned developer" heuristic relevant to each persona's domain.
* **Balancing Role (Mandate):** Critically, the diverse viewpoints are intended to provide balance, challenge assumptions, identify risks from multiple angles (technical, security, usability, strategic), and prevent skewed or incomplete solutions. This is essential for robust validation.
* **Output:** Structured feedback attributed to relevant personas, synthesized by the Overseer persona into actionable recommendations or analyses.
* **Strategic Meta-Loop:** The Core Team simulation forms the basis of the high-level strategic review cycle used for Co-Adaptive Protocol Evolution.

## 2. Apex Symbiotic Workflow (Drake <> Scribe/Ekko)

This workflow automates the code validation and integration process, minimizing manual Architect steps after the initial directive.

1.  **Directive & Code Generation (Drake):** Architect issues directive -> Drake generates complete code artifact (e.g., Python file).
2.  **Dispatch to Validation Agent (Drake -> Scribe/Ekko):**
    * **(Current - Scribe v1.1):** Drake generates the `python scribe_agent.py ...` command (with `--code-file` path or using `--target-file` for existing validation after Scribe fix). Architect executes this command.
    * **(Future - Ekko/Scribe API):** Drake makes a direct API call to the Scribe/Ekko service, passing code, target info, and flags.
3.  **Validation Gauntlet (Scribe/Ekko - Automated):**
    * Agent receives task.
    * Sets up isolated workspace/environment (checks out Git branch, ensures venv, installs deps).
    * Performs Dependency Security Audit (`pip audit`).
    * Applies code artifact (if provided).
    * Runs Static Analysis Suite: Format (`ruff format`), Lint (`ruff check --fix`), Type Check (`mypy`).
    * Runs AI-Driven Checks (Optional): Generates unit tests via LLM, executes tests (`pytest`), simulates AI code review via LLM.
    * Runs Project Checks: Executes `pre-commit run --files ...` if configured.
    * Compiles detailed JSON report of all step outcomes.
4.  **Analysis & Self-Correction Loop (Drake - Automated):**
    * Agent sends report back to Drake (via stdout/JSON for CLI Scribe, API response for future).
    * Drake parses the report.
    * **If FAILURE:** Drake analyzes errors -> Attempts automated code correction based on feedback -> Re-submits to Agent (goto Step 3, limited retries).
    * **If Persistent FAILURE:** Drake escalates to Architect with full context (code, reports, attempted fixes).
    * **If SUCCESS:** Proceed to next step.
5.  **Commit & Push (Scribe/Ekko - Conditional/Automated):**
    * If validation succeeded and commit was requested, Agent runs `git add`, `git commit`, `git push` (to integration branch). Reports SHA.
6.  **Deployment Trigger (Drake - Automated):**
    * If commit successful, Drake triggers the relevant CI/CD pipeline (e.g., GitHub Actions via webhook/API) for deployment.
7.  **CI/CD Pipeline Execution (External - Automated):**
    * Pipeline runs (build, test, deploy to staging/prod, smoke tests, rollback on failure). Reports status.
8.  **Final Reporting (Drake):**
    * Drake monitors deployment status and reports final success/failure to Architect.

*(This workflow utilizes the tools installed by `nexus_env_init.sh` and relies on the correct setup of project repositories with `pre-commit` and CI/CD configurations).*
