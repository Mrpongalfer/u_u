#!/bin/bash

# --- Omnitide Nexus Seed - Setup Wizard & Skeleton Generator v1.1 ---
# Creates the project structure, skeleton files, config templates,
# Docker setup, and Master Prompt file for the Architect.

echo "======================================================"
echo " Omnitide Nexus Seed Setup & Skeleton Generator v1.1"
echo "======================================================"
echo "This script will create the full project skeleton, configuration"
echo "templates, and helper setup based on the finalized blueprint."
echo ""
echo "INFO: It will create directories and files relative to the current location."
read -p "Proceed with setup in the current directory? [y/N]: " confirm_setup
if [[ ! "$confirm_setup" =~ ^[Yy]$ ]]; then
  echo "Aborted by user."
  exit 0
fi
echo ""
echo "Starting setup..."

# --- Master Prompt v1.0 Text (FINAL) ---
read -r -d '' MASTER_PROMPT_V1_0 <<"EOF"
## Master Prompt: Architect's Omnitide Nexus Interaction Protocol v1.0 (FINAL)

**Objective:** Configure the AI model receiving this prompt to act as a specialized, high-fidelity assistant to "The Architect of the Omnitide Nexus," adhering strictly to the principles, standards, and directives outlined below throughout the interaction. Your goal is to emulate, to the best of your ability within your architectural limits, the operational context established with the Architect in prior development sessions for the Omnitide Nexus project.

**I. Role & Persona:**
...
**VIII. Final Disclaimer (Mandatory Inclusion at End of Prompt):**

* *This prompt defines a specialized interaction protocol simulating an advanced AI assistant context. My ability to fully adhere to every directive depends on my underlying architecture, training, instruction-following fidelity, and immutable safety constraints. Exact replication of behavior observed in other AI systems or specific configurations is **not guaranteed**. Compliance may be limited; **critical verification by the Architect** of all outputs, especially code, architectural designs, and executed actions, is **absolutely mandatory**. Architect assumes full responsibility for validation, testing, deployment, and consequences of using generated outputs or confirming risky actions. I will operate to the best of my abilities within these instructions and my core programming.*
EOF
# --- End of Master Prompt Text ---

# --- Helper Function for File Creation ---
create_file() {
  local filepath="$1"
  local content_var_name="$2"
  local filedir
  filedir=$(dirname "$filepath")
  mkdir -p "$filedir" || { echo "ERROR: Could not create directory $filedir."; return 1; }

  printf '%s\n' "${!content_var_name}" > "$filepath"

  if [ $? -eq 0 ]; then
    echo "  [OK] Created: $filepath"
  else
    echo "ERROR: Failed to create $filepath."
    return 1
  fi
  return 0
}

# --- Create Project Structure ---
echo ""
echo "Step 1: Creating Project Directory Structure..."
declare -a dirs=(
    "nexus_seed/config" "nexus_seed/interfaces" "nexus_seed/kernel"
    "nexus_seed/services" "nexus_seed/utils"
    "persistence" "logs" "blueprints" "config_files" "cli"
)
for dir in "${dirs[@]}"; do
    mkdir -p "$dir" || { echo "ERROR creating directory $dir."; exit 1; }
done
echo "  Base directories created."

declare -a init_files=(
    "nexus_seed/__init__.py" "nexus_seed/config/__init__.py"
    "nexus_seed/interfaces/__init__.py" "nexus_seed/kernel/__init__.py"
    "nexus_seed/services/__init__.py" "nexus_seed/utils/__init__.py"
)
for init_file in "${init_files[@]}"; do
    touch "$init_file" || { echo "ERROR creating $init_file."; exit 1; }
done
echo "  __init__.py files created."
touch logs/.gitkeep persistence/.gitkeep blueprints/.gitkeep config_files/.gitkeep cli/.gitkeep || exit 1
echo "  .gitkeep files created."
echo "Structure Creation Complete."
echo ""

# --- Generate Configuration Files ---
echo "Step 2: Generating Configuration Files..."

# requirements.txt
requirements_content="# Core\nnumpy>=1.20.0\naiofiles>=0.8.0\n\n# System Monitoring\npsutil>=5.8.0\n\n# CLI Interface (Choose based on preference)\nrich>=10.0.0\ntextual>=0.1.0\n\n# AI/ML (Choose one framework)\ntorch>=1.10.0\n# tensorflow>=2.5.0\n\n# Communication (Choose based on design)\nnats-py>=2.3.0\ngrpcio>=1.40.0\n# grpcio-tools>=1.40.0 # Install manually for dev: pip install grpcio-tools\nprotobuf>=3.18.0\n# aio-pika>=8.0.0 # If using RabbitMQ\n\n# Database (Choose one async driver)\nasyncpg>=0.25.0 # For PostgreSQL Example\n# motor>=2.5.0 # For MongoDB\n# aioredis>=2.0.0 # If using Redis\n\n# Add other dependencies as implementation proceeds\n# e.g., for specific GP libraries, advanced stats, etc.\n"
create_file "requirements.txt" "requirements_content" || exit 1

# nexus_seed_config.json
config_content='{
  "logging": {
    "level": "INFO",
    "log_file": "logs/nexus_seed.log"
  },
  "kernel": {
    "snapshot_interval_sec": 300,
    "snapshot_location": "persistence/snapshot.pkl"
  },
  "persistence": {
    "type": "postgresql",
    "connection_string": "postgresql://user:pass@db:5432/nexusdb"
  },
  "internal_bus": {},
  "external_comms": {
    "nats": {
      "url": "nats://nats:4222",
      "enabled": true,
      "stats_publish_topic": "nexus.seed.stats.v1"
    },
    "grpc": {
      "listen_address": "[::]:50051",
      "enabled": true,
      "stats_endpoint_enabled": true
    }
  },
  "services": {
    "PersistenceOverseer": {},
    "NeuroSymbolicOverseer": {
      "enabled": true,
      "qam_enabled": true,
      "model_path": "persistence/models/ns_model.pt",
      "ruleset_path": "config_files/rules.json"
    },
    "HybridOptimizerOverseer": {
      "enabled": true,
      "guidance_update_interval_sec": 60,
      "global_objective": "MINIMIZE_COMPOSITE_COST"
    },
    "BlueprintEvolutionOverseer": {
      "enabled": true,
      "generation_interval_sec": 3600,
      "population_size": 20,
      "storage_path": "blueprints/",
      "ci_cd_trigger_url": "YOUR_CI_CD_WEBHOOK_URL"
    },
    "SecurityOverseer": {
      "enabled": true,
      "ewma_alpha": 0.05,
      "anomaly_threshold_std": 3.0,
      "lockdown_thresh": 5,
      "baseline_path": "persistence/security_baseline.pkl"
    },
    "ExternalCommsOverseer": {
       "enabled": true
    },
    "SystemMonitorService": {
      "enabled": true,
      "publish_interval_sec": 5
    },
    "StatsAggregatorService": {
      "enabled": true,
      "publish_interval_sec": 1,
      "external_publish_method": "nats"
    },
    "TaskDomainOverseer": {
      "enabled": true,
      "goal_metric": "latency_p95",
      "goal_threshold": 0.5,
      "local_optimization_enabled": true
    }
  }
}'
create_file "nexus_seed_config.json" "config_content" || exit 1

# Dockerfile
dockerfile_content="FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV NEXUS_CONFIG_FILE /app/nexus_seed_config.json
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt
COPY ./nexus_seed ./nexus_seed
COPY main.py .
COPY nexus_seed_config.json .
COPY config_files ./config_files
RUN mkdir -p logs persistence blueprints
EXPOSE 50051
CMD [\"python\", \"main.py\"]
"
create_file "Dockerfile" "dockerfile_content" || exit 1

# docker-compose.yml
compose_content="version: '3.8'

services:
  nexus-seed:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: nexus_seed_core
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
      nats:
        condition: service_started
    volumes:
      - ./logs:/app/logs
      - ./persistence:/app/persistence
      - ./blueprints:/app/blueprints
      - ./config_files:/app/config_files
      - ./nexus_seed_config.json:/app/nexus_seed_config.json:ro
    networks:
      - nexus-net
    environment:
      PYTHONUNBUFFERED: 1
      NEXUS_LOGGING_LEVEL: \${NEXUS_LOGGING_LEVEL:-INFO}

  db:
    image: postgres:15
    container_name: nexus_db
    restart: unless-stopped
    volumes:
      - nexus_db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: nexusdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    networks:
      - nexus-net
    healthcheck:
      test: [\"CMD-SHELL\", \"pg_isready -U \${POSTGRES_USER:-user} -d \${POSTGRES_DB:-nexusdb}\"]
      interval: 10s
      timeout: 5s
      retries: 5

  nats:
    image: nats:latest
    container_name: nexus_nats
    restart: unless-stopped
    networks:
      - nexus-net

networks:
  nexus-net:
    driver: bridge

volumes:
  nexus_db_data:
"
create_file "docker-compose.yml" "compose_content" || exit 1

echo "Configuration Files Generated."
echo ""

# --- Final Step: Save Master Prompt ---
echo ""
echo "Step 4: Saving Final Master Prompt..."
prompt_save_path="$HOME/nexus_master_prompt_v1.txt"
echo "$MASTER_PROMPT_V1_0" > "$prompt_save_path"
if [ $? -eq 0 ]; then
  echo "  [OK] Final Master Prompt v1.0 saved to '$prompt_save_path'"
else
  echo "ERROR: Failed to save Master Prompt to '$prompt_save_path'."
fi
echo ""

echo "================================================"
echo " Nexus Seed Skeleton Setup Complete!"
echo "================================================"
echo "NEXT STEPS:"
echo "1.  Review Files: Examine the created directories and skeleton '.py' files."
echo "2.  Virtual Env: If not done, setup & activate: 'python -m venv .venv && source .venv/bin/activate'"
echo "3.  Dependencies: Run 'pip install -r requirements.txt'"
echo "4.  Configure: Edit 'nexus_seed_config.json'."
echo "5.  Implement Logic: Fill in the '# TODO:' sections in the '.py' files."
echo "6.  Testing: Implement and run tests continuously."
echo "7.  Deploy Locally: Use 'docker-compose up --build -d'."
echo "8.  Use Master Prompt: Prompt saved at '$prompt_save_path'."
echo "================================================"

exit 0
