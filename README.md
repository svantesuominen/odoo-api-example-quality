# Odoo Quality Alert Automation

This project provides a Python script to programmatically create Quality Alerts in an Odoo v19e environment using the JSON-RPC API. It is designed to demonstrate how to authenticate and interact with Odoo external APIs using standard Python libraries.

## 🚀 Setup & Configuration

### 1. Environment Variables
This script **requires** a `.env` file to function. It will exit with an error if variables are missing. Create a file named `.env` in the project root (this file is git-ignored by default) and add the following details:

```ini
ODOO_HOST=https://your-odoo-instance.com
ODOO_DB=your-database-name
ODOO_USER=your-username@example.com
ODOO_API_KEY=your-api-key
```

### 2. Getting an API Key
You should not use your account password for scripts. Instead, generate a dedicated API Key:
1.  Log in to your Odoo instance.
2.  Go to **Preferences** (click your avatar in the top right).
3.  Click the **Account Security** tab.
4.  Click **New API Key**, verify your password, and give it a Description (e.g., "Python Automation").
5.  Copy the key generated.

For more details, refer to the [Official Odoo External API Documentation](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html#api-keys).

### 3. Installation
It is recommended to use a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate and install dependencies (only 'requests' is needed)
./venv/bin/pip install requests
```

## 🛠 Usage

Run the script using your virtual environment's Python:

```bash
./venv/bin/python create_quality_alert.py
```

The script will:
1.  Authenticate with the Odoo server using the credentials in `.env`.
2.  Prompt you for a **Quality Alert Title** (optional; defaults to "New Quality Alert (API)").
3.  Create the record in the `quality.alert` model.
4.  Output the ID of the new record upon success.

## ℹ️ Credits

Created by **Svante** and **Google Antigravity**.
