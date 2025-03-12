#!/usr/bin/env python3

import os
import json

# --- Configuration ---
PROJECT_ROOT_DIR = "termux-unconventional-utils"
INSTALLER_DIR_NAME = "installer"
MODULES_DIR_NAME = "modules"
TEMPLATES_DIR_NAME = "templates"

FRAMEWORK_CONFIG_FILE_NAME = "framework_config.json"
MODULES_CONFIG_FILE_NAME = "modules.json"
OBSERVER_DASHBOARD_CONFIG_FILE_NAME = "observer_dashboard_config.json"
SWARM_AGENT_CONFIG_FILE_NAME = "swarm_agent_config.json"
UNCONVENTIONAL_UTILITIES_SCRIPT_NAME = "unconventional_utilities.py"
NETWORK_MONITOR_BOT_SCRIPT_NAME = "network_monitor_bot.py"
UNINSTALL_SCRIPT_NAME = "uninstall_unconventional_utils.sh"
OBSERVER_DASHBOARD_SCRIPT_NAME = "observer_dashboard.py"
SWARM_AGENT_SCRIPT_NAME = "swarm_agent.py"


MODULE_NAMES = [
    "rick_reality_warp",
    "rocket_scavenge_weaponize",
    "power_blood_data",
    "makima_control_suite",
    "momo_occult_anomalies",
    "serpents_network_aegis"
]

# --- Default File Contents ---
DEFAULT_FRAMEWORK_CONFIG = {}
DEFAULT_MODULES_CONFIG = {}
DEFAULT_OBSERVER_DASHBOARD_CONFIG = {}
DEFAULT_SWARM_AGENT_CONFIG = {}

DEFAULT_UNCONVENTIONAL_UTILITIES_CONTENT = """#!/usr/bin/env python3

import json
import os

# --- Configuration ---
FRAMEWORK_CONFIG_FILE = "framework_config.json"
MODULES_DIR = "modules"
MODULES_CONFIG_FILE = "modules.json" # Optional - for dynamic module discovery

# --- Load Framework Configuration ---
def load_framework_config():
    try:
        with open(FRAMEWORK_CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# --- Load Modules Configuration (Optional) ---
def load_modules_config():
    modules_config_path = os.path.join(MODULES_DIR, MODULES_CONFIG_FILE)
    if os.path.exists(modules_config_path):
        try:
            with open(modules_config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {MODULES_CONFIG_FILE}. Please check the file for errors.")
            return {}
    return {}

# --- Module Management ---
def list_modules():
    module_dirs = [d for d in os.listdir(MODULES_DIR)
                   if os.path.isdir(os.path.join(MODULES_DIR, d)) and not d.startswith('.')]
    return module_dirs

def load_module(module_name):
    try:
        module_script_path = os.path.join(MODULES_DIR, module_name, f"{module_name.replace('_', '')}_module.py") # e.g., rick_reality_warp -> rickrealitywarp_module.py
        if os.path.exists(module_script_path):
            module = __import__(f"modules.{module_name}.{module_name.replace('_', '')}_module", fromlist=['*']) # Dynamic import
            return module
        else:
            print(f"Error: Module script not found at {module_script_path}")
            return None
    except ImportError as e:
        print(f"Error importing module {module_name}: {e}")
        return None

# --- Natural Language Processing (Basic Keyword-Based Intent Recognition) ---
def process_natural_language_command(command_text):
    command_text = command_text.lower() # Normalize input

    if "scan network" in command_text:
        module = load_module("serpents_network_aegis")
        if module and hasattr(module, 'perform_network_scan'): # Example function in Serpent's Aegis module
            print("Executing Network Scan from Serpent's Aegis Module...")
            module.perform_network_scan() # Example function call - adjust as needed
            return True
        else:
            print("Error: Network Scan functionality not available or module not loaded.")
            return False

    elif "translate" in command_text and "text" in command_text:
        module = load_module("rick_reality_warp")
        if module and hasattr(module, 'translate_text'): # Example function in Rick's Reality Warp module
            text_to_translate = input("Enter text to translate: ") # Get user input for translation
            target_language = input("Enter target language: ")
            print(f"Translating text to {target_language} using Rick's Reality Warp Module...")
            module.translate_text(text_to_translate, target_language) # Example function call - adjust as needed
            return True
        else:
            print("Error: Text Translation functionality not available or module not loaded.")
            return False

    elif "urban legends" in command_text or "folklore" in command_text:
        module = load_module("momo_occult_anomalies")
        if module and hasattr(module, 'query_urban_legend_database'): # Example function in Momo's module
            query = input("Enter search query for Urban Legend Database: ")
            print("Querying Urban Legend Database from Momo's Occult & Anomalies Module...")
            module.query_urban_legend_database(query) # Example function call - adjust as needed
            return True
        else:
            print("Error: Urban Legend Database functionality not available or module not loaded.")
            return False


    else:
        print("Unrecognized command. Try 'scan network', 'translate text', or 'urban legends'.")
        return False


# --- Main Framework Function ---
def main():
    framework_config = load_framework_config()
    modules_config = load_modules_config() # Optional

    print("\n--- Unconventional Utilities Framework ---")
    print("Loaded Modules:", list_modules()) # Display available modules

    while True:
        command = input("Enter command (or 'help' for options, 'exit' to quit): ").strip()

        if command.lower() == "help":
            print("\n--- Available Commands ---")
            print("- help: Show this help message")
            print("- list modules: List installed modules")
            print("- <module_name> <tool_name> [options]: Execute a specific tool from a module (e.g., rick_reality_warp interdimensional_data_access --url <url>)") # Direct module/tool execution - to be implemented
            print("- <natural language command>:  Use natural language to execute actions (e.g., 'scan network', 'translate text')")
            print("- exit: Quit the framework")
            print("\n--- Example Natural Language Commands ---")
            print("- scan network")
            print("- translate text")
            print("- urban legends")
            print("\n---")


        elif command.lower() == "list modules":
            print("Installed Modules:", list_modules())

        elif command.lower() == "exit":
            print("Exiting Framework.")
            break


        elif command.lower().startswith("rick") or command.lower().startswith("rocket") or command.lower().startswith("power") or command.lower().startswith("makima") or command.lower().startswith("momo") or command.lower().startswith("serpents"): # Direct Module Command - to be implemented in next iterations
            print("Direct module command execution is under development. Use natural language commands for now.")


        else: # Assume it's a natural language command
             process_natural_language_command(command)


if __name__ == "__main__":
    main()
"""

DEFAULT_NETWORK_MONITOR_BOT_CONTENT = """#!/usr/bin/env python3

import time
import subprocess
import json
import os

# --- Configuration ---
MONITOR_INTERVAL = 60  # seconds
LOG_FILE = "network_monitor.log"
CONFIG_FILE = "network_monitor_config.json"

DEFAULT_CONFIG = {
    "network_interface": "wlan0", # Adjust as needed for Termux
    "ping_target": "8.8.8.8", # Google Public DNS
    "firewall_enabled": False, # Initially disabled
    "anomaly_detection_enabled": False # Initially disabled
}


# --- Logging Function ---
def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\\n"
    with open(LOG_FILE, "a") as logfile:
        logfile.write(log_entry)
    print(log_entry.strip()) # Also print to console


# --- Load Configuration ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            log_message(f"Error: Could not decode JSON from {CONFIG_FILE}. Using default config.")
            return DEFAULT_CONFIG
    else:
        return DEFAULT_CONFIG


# --- Network Monitoring Functions ---

def check_network_connectivity(config):
    ping_target = config.get("ping_target", DEFAULT_CONFIG["ping_target"])
    try:
        subprocess.check_output(["ping", "-c", "1", ping_target], timeout=5) # 1 ping packet, 5 sec timeout
        return True
    except subprocess.TimeoutExpired:
        log_message(f"Warning: Ping to {ping_target} timed out. Network connectivity issue?")
        return False
    except subprocess.CalledProcessError:
        log_message(f"Warning: Ping to {ping_target} failed. Network down?")
        return False
    except Exception as e:
        log_message(f"Error checking network connectivity: {e}")
        return False


def get_signal_strength(interface):
    try:
        output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True) # Requires termux-api
        signal_strength_line = next((line for line in output.splitlines() if "signal_strength:" in line), None)
        if signal_strength_line:
            strength = signal_strength_line.split(":")[1].strip()
            return strength
        else:
            log_message("Warning: Signal strength not found in termux-wifi-connectioninfo output.")
            return "N/A"
    except FileNotFoundError:
        log_message("Warning: termux-api not installed. Cannot get signal strength.")
        return "N/A"
    except Exception as e:
        log_message(f"Error getting signal strength: {e}")
        return "N/A"


# --- Basic Firewall (iptables) - Termux Environment ---
def enable_firewall(config):
    if not config.get("firewall_enabled"):
        log_message("Enabling basic firewall (iptables)...")
        try:
            subprocess.run(["iptables", "-A", "INPUT", "-j", "DROP"]) # Drop all incoming connections (basic - refine later)
            subprocess.run(["iptables", "-A", "OUTPUT", "-j", "DROP"]) # Drop all outgoing connections (basic - refine later)
            subprocess.run(["iptables", "-A", "INPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"]) # Allow established/related incoming
            subprocess.run(["iptables", "-A", "OUTPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"]) # Allow established/related outgoing
            subprocess.run(["iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"]) # Allow loopback
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"]) # Allow loopback

            config["firewall_enabled"] = True
            save_config(config)
            log_message("Basic firewall enabled.")

        except FileNotFoundError:
            log_message("Warning: iptables not found. Firewall functionality not available in this Termux environment.")
        except Exception as e:
            log_message(f"Error enabling firewall: {e}")


def disable_firewall(config):
    if config.get("firewall_enabled"):
        log_message("Disabling firewall (iptables)...")
        try:
            subprocess.run(["iptables", "-F"]) # Flush all rules
            subprocess.run(["iptables", "-X"]) # Delete all chains
            subprocess.run(["iptables", "-P", "INPUT", "ACCEPT"]) # Set default INPUT policy to ACCEPT
            subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"]) # Set default OUTPUT policy to ACCEPT
            subprocess.run(["iptables", "-P", "FORWARD", "ACCEPT"]) # Set default FORWARD policy to ACCEPT

            config["firewall_enabled"] = False
            save_config(config)
            log_message("Firewall disabled.")

        except FileNotFoundError:
            log_message("Warning: iptables not found. Cannot disable firewall.")
        except Exception as e:
            log_message(f"Error disabling firewall: {e}")


# --- Configuration Save Function ---
def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        log_message(f"Error saving config to {CONFIG_FILE}: {e}")


# --- Main Monitoring Loop ---
def main():
    config = load_config()
    log_message("Network Monitor Bot started.")

    if config.get("firewall_enabled"): # Check on startup if firewall should be enabled
        enable_firewall(config) # Ensure firewall is enabled if config says so

    try:
        while True:
            log_message("--- Network Monitoring Cycle ---")
            if check_network_connectivity(config):
                signal_strength = get_signal_strength(config.get("network_interface", DEFAULT_CONFIG["network_interface"]))
                log_message(f"Connectivity OK. Signal Strength: {signal_strength}")

                # --- Example Basic Anomaly Detection (Traffic Volume - Placeholder for AI) ---
                if config.get("anomaly_detection_enabled"):
                    # In future iterations, implement AI-driven anomaly detection here
                    log_message("Anomaly detection is currently a placeholder. AI integration pending.")


            else:
                log_message("Connectivity Problem Detected!")
                # --- Example Basic Automated Action (Restarting Network Interface - Placeholder for AI-Driven Optimization) ---
                log_message("Attempting to restart network interface (placeholder for AI-driven optimization)...")
                try:
                    interface = config.get("network_interface", DEFAULT_CONFIG["network_interface"])
                    subprocess.run(["ifconfig", interface, "down"])
                    time.sleep(5)
                    subprocess.run(["ifconfig", interface, "up"])
                    time.sleep(10)
                    if check_network_connectivity(config):
                        log_message("Network interface restart successful. Connectivity restored?")
                    else:
                        log_message("Network interface restart failed to restore connectivity.")
                except Exception as e:
                    log_message(f"Error restarting network interface: {e}")


            time.sleep(MONITOR_INTERVAL)

    except KeyboardInterrupt:
        log_message("Network Monitor Bot stopped by user.")
        if config.get("firewall_enabled"):
            disable_firewall(config) # Disable firewall on exit


if __name__ == "__main__":
    main()
"""

DEFAULT_UNINSTALL_SCRIPT_CONTENT = """#!/bin/bash

# --- Uninstall Script for Unconventional Utilities Framework ---

PROJECT_ROOT_DIR="$HOME/termux-unconventional-utils"

echo "Uninstalling Unconventional Utilities Framework..."

# --- Stop any running background processes (if applicable - add process management later) ---
echo "Stopping any background processes..."
# Placeholder for process stopping commands (e.g., pkill -f network_monitor_bot.py)
echo "Background processes stopped (placeholder)."


# --- Remove project directory and all its contents ---
echo "Removing project directory: $PROJECT_ROOT_DIR"
rm -rf "$PROJECT_ROOT_DIR"

if [ $? -eq 0 ]; then
  echo "Unconventional Utilities Framework uninstalled successfully."
else
  echo "Error: Failed to uninstall completely. Please check for any remaining files in $PROJECT_ROOT_DIR"
fi

echo "Uninstallation complete."
"""

DEFAULT_DASHBOARD_HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <title>Observer Dashboard</title>
    <style>
        body { font-family: sans-serif; }
        .log-entry { margin-bottom: 0.5em; padding: 0.5em; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <h1>Observer Dashboard</h1>
    <div id="log-container">
        </div>

    <script>
        function addLogEntry(message) {
            const logContainer = document.getElementById('log-container');
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.textContent = message;
            logContainer.prepend(logEntry); // Add new logs at the top
        }

        function fetchLogs() {
            fetch('/get_logs') // Flask route to get logs - to be implemented in observer_dashboard.py
                .then(response => response.json())
                .then(data => {
                    if (data && data.logs) {
                        data.logs.forEach(log => addLogEntry(log));
                    }
                })
                .catch(error => console.error('Error fetching logs:', error));
        }

        // Fetch logs initially and then every 5 seconds (adjust interval as needed)
        fetchLogs();
        setInterval(fetchLogs, 5000); // 5000 milliseconds = 5 seconds
    </script>
</body>
</html>
"""

DEFAULT_ERROR_HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>An Error Occurred</h1>
    <p>Sorry, something went wrong.</p>
    <p id="error-message"></p>

    <script>
        // Set error message from URL parameter if available
        const urlParams = new URLSearchParams(window.location.search);
        const errorMessage = urlParams.get('message');
        if (errorMessage) {
            document.getElementById('error-message').textContent = "Error details: " + errorMessage;
        }
    </script>
</body>
</html>
"""


# --- Installer Functions ---

def create_directories():
    os.makedirs(PROJECT_ROOT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT_DIR, INSTALLER_DIR_NAME), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT_DIR, MODULES_DIR_NAME), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT_DIR, TEMPLATES_DIR_NAME), exist_ok=True)

    for module_name in MODULE_NAMES:
        os.makedirs(os.path.join(PROJECT_ROOT_DIR, MODULES_DIR_NAME, module_name), exist_ok=True)
        os.makedirs(os.path.join(PROJECT_ROOT_DIR, MODULES_DIR_NAME, module_name, "config"), exist_ok=True)
        os.makedirs(os.path.join(PROJECT_ROOT_DIR, MODULES_DIR_NAME, module_name, "data"), exist_ok=True)


def create_files():
    # Framework Config files
    _create_json_file(os.path.join(PROJECT_ROOT_DIR, FRAMEWORK_CONFIG_FILE_NAME), DEFAULT_FRAMEWORK_CONFIG)
    _create_json_file(os.path.join(PROJECT_ROOT_DIR, MODULES_CONFIG_FILE_NAME), DEFAULT_MODULES_CONFIG)
    _create_json_file(os.path.join(PROJECT_ROOT_DIR, OBSERVER_DASHBOARD_CONFIG_FILE_NAME), DEFAULT_OBSERVER_DASHBOARD_CONFIG)
    _create_json_file(os.path.join(PROJECT_ROOT_DIR, SWARM_AGENT_CONFIG_FILE_NAME), DEFAULT_SWARM_AGENT_CONFIG)

    # Scripts
    _create_script_file(os.path.join(PROJECT_ROOT_DIR, UNCONVENTIONAL_UTILITIES_SCRIPT_NAME), DEFAULT_UNCONVENTIONAL_UTILITIES_CONTENT)
    _create_script_file(os.path.join(PROJECT_ROOT_DIR, NETWORK_MONITOR_BOT_SCRIPT_NAME), DEFAULT_NETWORK_MONITOR_BOT_CONTENT)
    _create_script_file(os.path.join(PROJECT_ROOT_DIR, UNINSTALL_SCRIPT_NAME), DEFAULT_UNINSTALL_SCRIPT_CONTENT, executable=True) # Uninstall script is executable
    _create_script_file(os.path.join(PROJECT_ROOT_DIR, OBSERVER_DASHBOARD_SCRIPT_NAME), "# Placeholder for observer_dashboard.py") # Placeholder - implement later
    _create_script_file(os.path.join(PROJECT_ROOT_DIR, SWARM_AGENT_SCRIPT_NAME), "# Placeholder for swarm_agent.py") # Placeholder - implement later


    # Templates
    _create_html_file(os.path.join(PROJECT_ROOT_DIR, TEMPLATES_DIR_NAME, "dashboard.html"), DEFAULT_DASHBOARD_HTML_CONTENT)
    _create_html_file(os.path.join(PROJECT_ROOT_DIR, TEMPLATES_DIR_NAME, "error.html"), DEFAULT_ERROR_HTML_CONTENT)


    # Module files
    for module_name in MODULE_NAMES:
        _create_script_file(os.path.join(PROJECT_ROOT_DIR, MODULES_DIR_NAME, module_name, f"{module_name.replace('_', '')}_module.py"), "# Placeholder for module script") # Module script placeholder
        _create_json_file(os.path.join(PROJECT_ROOT_DIR, MODULES_DIR_NAME, module_name, "config", "config.json"), {}) # Empty module config
        _create_markdown_file(os.path.join(PROJECT_ROOT_DIR, MODULES_DIR_NAME, module_name, "README.md"), f"## {module_name.replace('_', ' ').title()} Module\\n\\nDescription: Placeholder description for {module_name.replace('_', ' ').title()} module.\\n\\nTools:\\n- Tool 1: Placeholder\\n- Tool 2: Placeholder\\n\\nUsage:\\n\\nConfiguration:\\n") # Basic README


# --- Helper Functions for File Creation ---
def _create_json_file(filepath, content):
    with open(filepath, "w") as f:
        json.dump(content, f, indent=4)
    print(f"Created JSON file: {filepath}")

def _create_script_file(filepath, content, executable=False):
    with open(filepath, "w") as f:
        f.write(content)
    if executable:
        os.chmod(filepath, 0o755) # Make executable
    print(f"Created script file: {filepath} (Executable: {executable})")

def _create_html_file(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Created HTML file: {filepath}")

def _create_markdown_file(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Created Markdown file: {filepath}")


# --- Main Installer Function ---
def main():
    print("--- Starting Unconventional Utilities Framework Installer ---")

    create_directories()
    print("Directories created.")

    create_files()
    print("Files populated.")

    print(f"\nUnconventional Utilities Framework installed successfully in ~/{PROJECT_ROOT_DIR}")
    print(f"Run the framework using:  ~/{PROJECT_ROOT_DIR}/{UNCONVENTIONAL_UTILITIES_SCRIPT_NAME}")
    print(f"Uninstall using:          ~/{PROJECT_ROOT_DIR}/{UNINSTALL_SCRIPT_NAME}")
    print("\n--- Installation Complete ---")


if __name__ == "__main__":
    main()
