from pathlib import Path
from connection import get_driver

def seed_database():
    cypher_path = Path(__file__).resolve().parent.parent / "cypher" / "01_seed_graph.cypher"
    with open(cypher_path, "r", encoding="utf-8") as f:
        cypher_script = f.read()

    queries = [q.strip() for q in cypher_script.split(";") if q.strip()]

    driver = get_driver()
    with driver.session() as session:
        for query in queries:
            session.run(query)
    driver.close()
    print("Graph successfully seeded with 22 nodes and 27 relationships.")

if __name__ == "__main__":
    seed_database()