import os
import time
from pathlib import Path
from dotenv import load_dotenv
from neo4j import Driver, GraphDatabase

# Load .env from the 04-supply-chain-kg directory
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


def get_driver() -> Driver:
    """Create and validate a Neo4j Bolt/AuraDB driver instance."""
    missing = [
        name
        for name, val in [
            ("NEO4J_URI", URI),
            ("NEO4J_USERNAME", USER),
            ("NEO4J_PASSWORD", PASSWORD),
        ]
        if not val or "<your-" in val
    ]
    if missing:
        raise ValueError(
            f"Missing or unconfigured Neo4j environment variables in .env: {', '.join(missing)}"
        )

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    last_err = None
    for attempt in range(4):
        try:
            driver.verify_connectivity()
            return driver
        except Exception as err:
            last_err = err
            if attempt < 3:
                time.sleep(1.0)
    if last_err:
        raise last_err
    return driver
