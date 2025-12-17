"""
Configuration (.env):
ODOO_HOST=https://your-odoo-instance.com
ODOO_DB=your-db-name
ODOO_USER=your-email@example.com
ODOO_API_KEY=your-api-key
"""
import requests
import json
import random
import sys
import os

# -------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------
# Simple .env loader to avoid external dependencies for this example
def load_env():
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

load_env()

USERNAME = os.getenv("ODOO_USER")
API_KEY = os.getenv("ODOO_API_KEY")

# Environment Details
HOST = os.getenv("ODOO_HOST")
DB = os.getenv("ODOO_DB")

if not all([USERNAME, API_KEY, HOST, DB]):
    print("Error: ODOO_USER, ODOO_API_KEY, ODOO_HOST, and ODOO_DB must be set in .env")
    sys.exit(1)
ENDPOINT = f"{HOST}/jsonrpc"

# Target Details
MODEL = "quality.alert"
TEAM_ID = 1

def json_rpc(url, service, method, args):
    """
    Helper to make JSON-RPC calls to the Odoo instance.
    Adapts the XML-RPC style logic to the JSON-RPC endpoint.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args,
        },
        "id": random.randint(0, 1000000000),
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        sys.exit(1)

    if "error" in result:
        print(f"Odoo RPC Error: {json.dumps(result['error'], indent=2)}")
        sys.exit(1)
        
    return result["result"]

def main():
    print("--- Odoo v19e JSON-RPC Automation ---")
    
    # 1. Authentication (Login)
    # Service: common
    # Method: login
    # Args: db, login, password
    print(f"Authenticating as {USERNAME} on {DB}...")
    
    # Try 'login' first
    uid = json_rpc(ENDPOINT, "common", "login", [DB, USERNAME, API_KEY])

    # If login fails (returns None or False), try 'authenticate'
    if not uid:
        print("Login failed or returned False. Trying 'authenticate'...")
        uid = json_rpc(ENDPOINT, "common", "authenticate", [DB, USERNAME, API_KEY, {}])
        print(f"Authenticate result: {uid}")
    
    if not uid:
        print("Authentication failed. Please check your credentials.")
        sys.exit(1)
        
    print(f"Authentication successful. User ID: {uid}")

    # Prompt user for title
    print("\n--- Alert Details ---")
    alert_title = input("Enter Quality Alert Title (press Enter for default): ").strip()
    if not alert_title:
        alert_title = "New Quality Alert (API)"

    alert_desc = input("Enter Description (press Enter for default): ").strip()
    if not alert_desc:
        alert_desc = "Created via JSON-RPC script."

    # 2. Define payload for the new record
    # Common fields for quality.alert:
    # - product_id: ID of the product (int) or False
    # - product_tmpl_id: ID of the product template (int) or False
    # - user_id: ID of the responsible user (int) or False
    # - priority: '0' (Normal), '1' (Low), '2' (High), '3' (Very High)
    # - partner_id: ID of the partner (int) or False
    new_alert_data = {
        "name": alert_title,
        "description": alert_desc,
        "team_id": TEAM_ID,
        
        # Placeholders for other common fields (set to False or valid IDs)
        "product_id": False,       # e.g., 10
        "product_tmpl_id": False,  # e.g., 5
        "user_id": uid,            # Assign to current user by default
        "priority": "0",           
        "partner_id": False,
    }

    # 3. Create Record
    # Service: object
    # Method: execute_kw
    # Args: db, uid, password, model_name, method_name, arguments_list
    # Note: 'create' method expects a list of dicts (usually just one dict)
    print(f"Creating new {MODEL}...")
    
    record_id = json_rpc(ENDPOINT, "object", "execute_kw", [
        DB, 
        uid, 
        API_KEY, 
        MODEL, 
        "create", 
        [new_alert_data]
    ])

    if record_id:
        print(f"SUCCESS: Created {MODEL} with ID {record_id}")
    else:
        print("Failed to create record.")

if __name__ == "__main__":
    main()
