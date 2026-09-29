# 🔌 01. Dev Environment & Driver Connection Verification

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Neo4j Driver](https://img.shields.io/badge/neo4j--driver-5.x-008CC1.svg)](https://neo4j.com/docs/python-manual/current/)
[![Security](https://img.shields.io/badge/dotenv-Credential%20Isolation-green.svg)]()

This project sets up the foundational environment for securely connecting Python applications to a **Neo4j Aura Cloud Database** (or local instance). It establishes driver connectivity, validates TLS/SSL handshakes, tests authentication, and executes lightweight Cypher health check queries.

---

## 🎯 Objectives & Learning Outcomes

1. **Virtual Environment Isolation**: Set up isolated Python dependencies without polluting system Python packages.
2. **Credential Protection**: Utilize `.env` file management with `python-dotenv` to eliminate hardcoded database credentials.
3. **Driver Connection Lifecycle**: Instantiate the official `neo4j.GraphDatabase.driver` object with `neo4j+s://` protocol.
4. **Robust Exception Handling**: Catch specific Neo4j exceptions (`AuthError`, `ServiceUnavailable`) to provide actionable diagnostic feedback.

---

## 🏗️ Architecture & Component Breakdown

```text
01-dev-environment-setup/
├── .env.example            # Public template for environment variables
├── .gitignore              # Ignores .env, .venv, and cache files
├── requirements.txt        # Package dependencies (neo4j, python-dotenv)
├── verify_connection.py    # Main Python script performing connection & health checks
├── README.md               # Detailed module documentation

```

### Key Python Dependencies
- **[`neo4j`](https://pypi.org/project/neo4j/)**: Official Neo4j Bolt driver for Python.
- **[`python-dotenv`](https://pypi.org/project/python-dotenv/)**: Reads key-value pairs from `.env` and sets them as system environment variables.

---
## Base Installations & Verification

1. Ensure **Python 3.10+**, **Git**, and **VS Code** are installed.
2. In VS Code, install the official **Python extension** (by Microsoft) from the Extensions Marketplace (`Ctrl + Shift + X` / `Cmd + Shift + X` on macOS).
3. Open a new terminal in VS Code (``Ctrl + ` `` or ``Cmd + ` `` on macOS) and verify the CLI installations:

```bash
python --version
pip --version
git --version
```

## Configure global Git identity if you haven't already:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"

## 🔍 Code Deep Dive: `verify_connection.py`
```

The core script [`verify_connection.py`](verify_connection.py) performs 4 sequential verification steps:

```python
import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable

# 1. Load environment variables from .env
load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def test_connection():
    # 2. Initialize Neo4j Driver Context Manager
    with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
        # 3. Perform TLS Handshake & Auth Verification
        driver.verify_connectivity()
        
        # 4. Execute Cypher Ping Query
        records, summary, _ = driver.execute_query(
            "RETURN 'Neo4j connection active and healthy!' AS status"
        )
        print(f"Query Result: {records[0]['status']}")
        print(f"Database Server: {summary.server.agent}")
```

### Why `verify_connectivity()`?
Calling `driver.verify_connectivity()` checks network routing, SSL certificate validity, and credentials before attempting to execute database queries, preventing application hangs or unhandled socket timeouts.

---

## ⚡ Step-by-Step Setup & Execution

### Step 1: Create & Activate Virtual Environment
```bash
# Navigate to module directory
cd 01-dev-environment-setup

# Create virtual environment
python -m venv .venv

# Activate environment
# On Windows PowerShell:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure `.env` File
Create a `.env` file in `01-dev-environment-setup/`:
```env
NEO4J_URI=neo4j+s://<your-aura-instance-id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your-aura-password>
```

### Step 4: Run Verification Script
```bash
python verify_connection.py
```

#### Expected Success Output:
```text
Connecting to Neo4j Aura...
 Connected to Neo4j Aura successfully!
 Query Result: Neo4j connection active and healthy!
 Database Server: Neo4j/5.x-aura
```
## Git Initialization & GitHub Push

1. Initialize Git in the project root:

```bash
git init
git add .
git commit -m "Initial commit: environment setup and Neo4j connectivity verification"
```
## Create a new repository on GitHub (keep it empty, without README or license).

## Link your local project to GitHub and push:
```bash
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```
## Note: VS Code will open a browser prompt to authenticate with your GitHub account if you haven't already signed in. Alternatively, verify or authenticate using GitHub CLI:
```bash
gh auth login
gh auth status
```
## 🎤 How to Explain This Project to Technical Reviewers

- **For Technical Screeners**: *"In this module, I set up the driver layer for Neo4j in Python. I used `python-dotenv` to separate configuration from code and implemented context-managed driver instances. I also included specific exception handling for `AuthError` and `ServiceUnavailable` to handle connection failures gracefully."*
- **For Non-Technical Managers**: *"This initial module ensures our Python application can talk securely to our cloud database in Neo4j Aura, testing authentication and server health before any business logic runs."*
