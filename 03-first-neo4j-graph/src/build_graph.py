from pathlib import Path
from connection import get_driver

SEED_CYPHER_STATEMENTS = [
    'MERGE (s:Student {id: "S01"}) ON CREATE SET s.name = "Aarav Sharma", s.level = "Beginner"',
    'MERGE (s:Student {id: "S02"}) ON CREATE SET s.name = "Elena Rostova", s.level = "Intermediate"',
    'MERGE (s:Student {id: "S03"}) ON CREATE SET s.name = "Chen Wei", s.level = "Advanced"',
    'MERGE (s:Student {id: "S04"}) ON CREATE SET s.name = "Maya Patel", s.level = "Intermediate"',
    'MERGE (s:Student {id: "S05"}) ON CREATE SET s.name = "Liam O\'Connor", s.level = "Beginner"',
    'MERGE (s:Student {id: "S06"}) ON CREATE SET s.name = "Zara Khan", s.level = "Advanced"',
    'MERGE (m:Mentor {id: "M01"}) ON CREATE SET m.name = "Dr. Alicia Vance", m.field = "Graph Data Science"',
    'MERGE (m:Mentor {id: "M02"}) ON CREATE SET m.name = "David Kim", m.field = "Cloud Infrastructure"',
    'MERGE (m:Mentor {id: "M03"}) ON CREATE SET m.name = "Sarah Jenkins", m.field = "Full-Stack Development"',
    'MERGE (c:Course {code: "CS101"}) ON CREATE SET c.title = "Neo4j & Knowledge Graphs", c.credits = 4',
    'MERGE (c:Course {code: "CS102"}) ON CREATE SET c.title = "Full-Stack Python APIs", c.credits = 3',
    'MERGE (c:Course {code: "CS103"}) ON CREATE SET c.title = "Distributed Cloud Architectures", c.credits = 4',
    'MERGE (sk:Skill {name: "Cypher"}) ON CREATE SET sk.category = "Database"',
    'MERGE (sk:Skill {name: "Python"}) ON CREATE SET sk.category = "Language"',
    'MERGE (sk:Skill {name: "Docker"}) ON CREATE SET sk.category = "DevOps"',
    'MERGE (sk:Skill {name: "GraphQL"}) ON CREATE SET sk.category = "API"',
    'MERGE (p:Project {id: "P01"}) ON CREATE SET p.name = "Enterprise Graph Engine", p.difficulty = "High"',
    'MERGE (p:Project {id: "P02"}) ON CREATE SET p.name = "E-Commerce Recommender", p.difficulty = "Medium"',
    'MERGE (p:Project {id: "P03"}) ON CREATE SET p.name = "Cloud Container Deployer", p.difficulty = "High"',
    'MERGE (co:Company {id: "C01"}) ON CREATE SET co.name = "GraphTech Labs", co.location = "San Francisco"',
    'MERGE (co:Company {id: "C02"}) ON CREATE SET co.name = "NextGen Cloud", co.location = "Berlin"',
    'MERGE (co:Company {id: "C03"}) ON CREATE SET co.name = "DataFlow Systems", co.location = "Bengaluru"',
    'MATCH (m:Mentor {id: "M01"}), (c:Course {code: "CS101"}) MERGE (m)-[:TEACHES]->(c)',
    'MATCH (m:Mentor {id: "M02"}), (c:Course {code: "CS103"}) MERGE (m)-[:TEACHES]->(c)',
    'MATCH (m:Mentor {id: "M03"}), (c:Course {code: "CS102"}) MERGE (m)-[:TEACHES]->(c)',
    'MATCH (c:Course {code: "CS101"}), (sk:Skill {name: "Cypher"}) MERGE (c)-[:TEACHES_SKILL]->(sk)',
    'MATCH (c:Course {code: "CS101"}), (sk:Skill {name: "Python"}) MERGE (c)-[:TEACHES_SKILL]->(sk)',
    'MATCH (c:Course {code: "CS102"}), (sk:Skill {name: "Python"}) MERGE (c)-[:TEACHES_SKILL]->(sk)',
    'MATCH (c:Course {code: "CS102"}), (sk:Skill {name: "GraphQL"}) MERGE (c)-[:TEACHES_SKILL]->(sk)',
    'MATCH (c:Course {code: "CS103"}), (sk:Skill {name: "Docker"}) MERGE (c)-[:TEACHES_SKILL]->(sk)',
    'MATCH (s:Student {id: "S01"}), (c:Course {code: "CS101"}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.enrolledOn = "2026-01-10"',
    'MATCH (s:Student {id: "S02"}), (c:Course {code: "CS101"}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.enrolledOn = "2026-01-12"',
    'MATCH (s:Student {id: "S02"}), (c:Course {code: "CS102"}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.enrolledOn = "2026-02-01"',
    'MATCH (s:Student {id: "S03"}), (c:Course {code: "CS103"}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.enrolledOn = "2026-01-15"',
    'MATCH (s:Student {id: "S04"}), (c:Course {code: "CS102"}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.enrolledOn = "2026-02-10"',
    'MATCH (s:Student {id: "S05"}), (c:Course {code: "CS101"}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.enrolledOn = "2026-03-01"',
    'MATCH (s:Student {id: "S06"}), (c:Course {code: "CS103"}) MERGE (s)-[r:ENROLLED_IN]->(c) ON CREATE SET r.enrolledOn = "2026-01-20"',
    'MATCH (s:Student {id: "S01"}), (p:Project {id: "P02"}) MERGE (s)-[:BUILT]->(p)',
    'MATCH (s:Student {id: "S02"}), (p:Project {id: "P01"}) MERGE (s)-[:BUILT]->(p)',
    'MATCH (s:Student {id: "S03"}), (p:Project {id: "P03"}) MERGE (s)-[:BUILT]->(p)',
    'MATCH (s:Student {id: "S06"}), (p:Project {id: "P01"}) MERGE (s)-[:BUILT]->(p)',
    'MATCH (p:Project {id: "P01"}), (sk:Skill {name: "Cypher"}) MERGE (p)-[:USES]->(sk)',
    'MATCH (p:Project {id: "P01"}), (sk:Skill {name: "Python"}) MERGE (p)-[:USES]->(sk)',
    'MATCH (p:Project {id: "P02"}), (sk:Skill {name: "Python"}) MERGE (p)-[:USES]->(sk)',
    'MATCH (p:Project {id: "P02"}), (sk:Skill {name: "GraphQL"}) MERGE (p)-[:USES]->(sk)',
    'MATCH (p:Project {id: "P03"}), (sk:Skill {name: "Docker"}) MERGE (p)-[:USES]->(sk)',
    'MATCH (s:Student {id: "S01"}), (co:Company {id: "C01"}) MERGE (s)-[r:INTERESTED_IN]->(co) ON CREATE SET r.priority = "High"',
    'MATCH (s:Student {id: "S02"}), (co:Company {id: "C01"}) MERGE (s)-[r:INTERESTED_IN]->(co) ON CREATE SET r.priority = "Medium"',
    'MATCH (s:Student {id: "S03"}), (co:Company {id: "C02"}) MERGE (s)-[r:INTERESTED_IN]->(co) ON CREATE SET r.priority = "High"',
    'MATCH (s:Student {id: "S06"}), (co:Company {id: "C03"}) MERGE (s)-[r:INTERESTED_IN]->(co) ON CREATE SET r.priority = "High"'
]

def seed_database():
    cypher_path = Path(__file__).resolve().parent.parent / "cypher" / "01_seed_graph.cypher"
    if cypher_path.exists():
        with open(cypher_path, "r", encoding="utf-8") as f:
            cypher_script = f.read()
        queries = [q.strip() for q in cypher_script.split(";") if q.strip()]
    else:
        queries = SEED_CYPHER_STATEMENTS

    driver = get_driver()
    with driver.session() as session:
        for query in queries:
            session.run(query)
        node_res = session.run("MATCH (n) RETURN count(n) AS count").single()
        rel_res = session.run("MATCH ()-[r]->() RETURN count(r) AS count").single()
        nodes = node_res["count"] if node_res else 0
        rels = rel_res["count"] if rel_res else 0

    driver.close()
    print(f"Graph successfully seeded with {nodes} nodes and {rels} relationships.")

if __name__ == "__main__":
    seed_database()