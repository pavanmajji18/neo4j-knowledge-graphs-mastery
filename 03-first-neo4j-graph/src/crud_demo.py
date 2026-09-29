from connection import get_driver
from build_graph import seed_database

def run_crud():
    # Ensure graph database is seeded with required data
    seed_database()

    driver = get_driver()
    with driver.session() as session:
        # 1. CREATE: Add student S07 enrolled in CS101 using MERGE for both entities
        session.run("""
            MERGE (s:Student {id: "S07", name: "Lucas Vance", level: "Beginner"})
            MERGE (c:Course {code: "CS101", title: "Neo4j & Knowledge Graphs", credits: 4})
            MERGE (s)-[:ENROLLED_IN {enrolledOn: "2026-09-01"}]->(c)
        """)
        print("[CREATE] Added student S07 enrolled in CS101.")

        # 2. READ: Query across all 6 node labels and relationship patterns
        print("\n[READ 1] Students who built projects using Cypher (:Student, :Project, :Skill, :BUILT, :USES):")
        result = session.run("""
            MATCH (s:Student)-[:BUILT]->(p:Project)-[:USES]->(sk:Skill {name: "Cypher"})
            RETURN s.name AS student, p.name AS project, sk.name AS skill
        """)
        for record in result:
            print(f" - {record['student']} built '{record['project']}' using {record['skill']}")

        print("\n[READ 2] Mentors teaching courses and skills (:Mentor, :Course, :Skill, :TEACHES, :TEACHES_SKILL):")
        result = session.run("""
            MATCH (m:Mentor)-[:TEACHES]->(c:Course)-[:TEACHES_SKILL]->(sk:Skill)
            RETURN m.name AS mentor, c.code AS course, sk.name AS skill
        """)
        for record in result:
            print(f" - Mentor {record['mentor']} teaches {record['course']} covering {record['skill']}")

        print("\n[READ 3] Students interested in target companies (:Student, :Company, :INTERESTED_IN):")
        result = session.run("""
            MATCH (s:Student)-[:INTERESTED_IN]->(co:Company)
            RETURN s.name AS student, co.name AS company
        """)
        for record in result:
            print(f" - {record['student']} interested in {record['company']}")

        # 3. UPDATE: Promote student S01 level
        session.run("""
            MATCH (s:Student {id: "S01"})
            SET s.level = "Intermediate"
        """)
        print("\n[UPDATE] Updated S01 level to Intermediate.")

        # 4. DELETE: Cleanly detach and delete student S07
        session.run("""
            MATCH (s:Student {id: "S07"})
            DETACH DELETE s
        """)
        print("\n[DELETE] Detached and deleted student S07.")

    driver.close()

if __name__ == "__main__":
    run_crud()