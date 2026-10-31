import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def get_driver():
    """Return a Neo4j driver after validating required environment variables."""
    missing = [v for v in ("NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD") if not os.getenv(v)]
    if missing:
        raise ValueError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Please set them in your .env file or shell environment."
        )
    return GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
