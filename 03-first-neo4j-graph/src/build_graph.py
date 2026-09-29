from pathlib import Path
from connection import get_driver

SEED_CYPHER_STATEMENTS = [
    'MERGE (s1:Student {id: "S01"}) ON CREATE SET s1.name = "Aarav Sharma", s1.level = "Beginner"',
    'MERGE (s2:Student {id: "S02"}) ON CREATE SET s2.name = "Elena Rostova", s2.level = "Intermediate"',
    'MERGE (s3:Student {id: "S03"}) ON CREATE SET s3.name = "Chen Wei", s3.level = "Advanced"',
    'MERGE (s4:Student {id: "S04"}) ON CREATE SET s4.name = "Maya Patel", s4.level = "Intermediate"',
    'MERGE (s5:Student {id: "S05"}) ON CREATE SET s5.name = "Liam O\'Connor", s5.level = "Beginner"',
    'MERGE (s6:Student {id: "S06"}) ON CREATE SET s6.name = "Zara Khan", s6.level = "Advanced"',
    'MERGE (m1:Mentor {id: "M01"}) ON CREATE SET m1.name = "Dr. Alicia Vance", m1.field = "Graph Data Science"',
    'MERGE (m2:Mentor {id: "M02"}) ON CREATE SET m2.name = "David Kim", m2.field = "Cloud Infrastructure"',
    'MERGE (m3:Mentor {id: "M03"}) ON CREATE SET m3.name = "Sarah Jenkins", m3.field = "Full-Stack Development"',
    'MERGE (c1:Course {code: "CS101"}) ON CREATE SET c1.title = "Neo4j & Knowledge Graphs", c1.credits = 4',
    'MERGE (c2:Course {code: "CS102"}) ON CREATE SET c2.title = "Full-Stack Python APIs", c2.credits = 3',
    'MERGE (c3:Course {code: "CS103"}) ON CREATE SET c3.title = "Distributed Cloud Architectures", c3.credits = 4',
    'MERGE (sk1:Skill {name: "Cypher"}) ON CREATE SET sk1.category = "Database"',
    'MERGE (sk2:Skill {name: "Python"}) ON CREATE SET sk2.category = "Language"',
    'MERGE (sk3:Skill {name: "Docker"}) ON CREATE SET sk3.category = "DevOps"',
    'MERGE (sk4:Skill {name: "GraphQL"}) ON CREATE SET sk4.category = "API"',
    'MERGE (p1:Project {id: "P01"}) ON CREATE SET p1.name = "Enterprise Graph Engine", p1.difficulty = "High"',
    'MERGE (p2:Project {id: "P02"}) ON CREATE SET p2.name = "E-Commerce Recommender", p2.difficulty = "Medium"',
    'MERGE (p3:Project {id: "P03"}) ON CREATE SET p3.name = "Cloud Container Deployer", p3.difficulty = "High"',
    'MERGE (co1:Company {id: "C01"}) ON CREATE SET co1.name = "GraphTech Labs", co1.location = "San Francisco"',
    'MERGE (co2:Company {id: "C02"}) ON CREATE SET co2.name = "NextGen Cloud", co2.location = "Berlin"',
    'MERGE (co3:Company {id: "C03"}) ON CREATE SET co3.name = "DataFlow Systems", co3.location = "Bengaluru"',
    'MERGE (m1)-[:TEACHES]->(c1)',
    'MERGE (m2)-[:TEACHES]->(c3)',
    'MERGE (m3)-[:TEACHES]->(c2)',
    'MERGE (c1)-[:TEACHES_SKILL]->(sk1)',
    'MERGE (c1)-[:TEACHES_SKILL]->(sk2)',
    'MERGE (c2)-[:TEACHES_SKILL]->(sk2)',
    'MERGE (c2)-[:TEACHES_SKILL]->(sk4)',
    'MERGE (c3)-[:TEACHES_SKILL]->(sk3)',
    'MERGE (s1)-[r1:ENROLLED_IN]->(c1) ON CREATE SET r1.enrolledOn = "2026-01-10"',
    'MERGE (s2)-[r2:ENROLLED_IN]->(c1) ON CREATE SET r2.enrolledOn = "2026-01-12"',
    'MERGE (s2)-[r3:ENROLLED_IN]->(c2) ON CREATE SET r3.enrolledOn = "2026-02-01"',
    'MERGE (s3)-[r4:ENROLLED_IN]->(c3) ON CREATE SET r4.enrolledOn = "2026-01-15"',
    'MERGE (s4)-[r5:ENROLLED_IN]->(c2) ON CREATE SET r5.enrolledOn = "2026-02-10"',
    'MERGE (s5)-[r6:ENROLLED_IN]->(c1) ON CREATE SET r6.enrolledOn = "2026-03-01"',
    'MERGE (s6)-[r7:ENROLLED_IN]->(c3) ON CREATE SET r7.enrolledOn = "2026-01-20"',
    'MERGE (s1)-[:BUILT]->(p2)',
    'MERGE (s2)-[:BUILT]->(p1)',
    'MERGE (s3)-[:BUILT]->(p3)',
    'MERGE (s6)-[:BUILT]->(p1)',
    'MERGE (p1)-[:USES]->(sk1)',
    'MERGE (p1)-[:USES]->(sk2)',
    'MERGE (p2)-[:USES]->(sk2)',
    'MERGE (p2)-[:USES]->(sk4)',
    'MERGE (p3)-[:USES]->(sk3)',
    'MERGE (s1)-[ri1:INTERESTED_IN]->(co1) ON CREATE SET ri1.priority = "High"',
    'MERGE (s2)-[ri2:INTERESTED_IN]->(co1) ON CREATE SET ri2.priority = "Medium"',
    'MERGE (s3)-[ri3:INTERESTED_IN]->(co2) ON CREATE SET ri3.priority = "High"',
    'MERGE (s6)-[ri4:INTERESTED_IN]->(co3) ON CREATE SET ri4.priority = "High"'
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