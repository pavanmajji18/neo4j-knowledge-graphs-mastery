import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable

# Load variables from .env
load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([URI, USERNAME, PASSWORD]):
    print("❌ Error: Missing credentials in .env file.")
    sys.exit(1)

def test_connection():
    print("Connecting to Neo4j Aura...")
    try:
        with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
            # Verify driver-level connectivity
            driver.verify_connectivity()
            print(" Connected to Neo4j Aura successfully!")

            # Run a lightweight query to confirm query execution
            records, summary, _ = driver.execute_query(
                "RETURN 'Neo4j connection active and healthy!' AS status"
            )
            print(f" Query Result: {records[0]['status']}")
            print(f" Database Server: {summary.server.agent}")

    except AuthError:
        print("❌ Authentication failed: Please verify your username and password.")
    except ServiceUnavailable as e:
        print(f"❌ Connection failed: Unable to connect to host. Details: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_connection()
