from connection import get_driver

def run_crud():
    driver = get_driver()
    with driver.session() as session:
        # Create
        session.run("""
            MERGE (s:Student {id: "S07", name: "Lucas Vance", level: "Beginner"})
            WITH s
            MATCH (c:Course {code: "CS101"})
            MERGE (s)-[:ENROLLED_IN {enrolledOn: "2026-09-01"}]->(c)
        """)
        print("[CREATE] Added student S07 enrolled in CS101.")

        # Read
        print("\n[READ] Students building projects using Cypher:")
        result = session.run("""
            MATCH (s:Student)-[:BUILT]->(p:Project)-[:USES]->(sk:Skill {name: "Cypher"})
            RETURN s.name AS student, p.name AS project
        """)
        for record in result:
            print(f" - {record['student']} built '{record['project']}'")

        # Update
        session.run("""
            MATCH (s:Student {id: "S01"})
            SET s.level = "Intermediate"
        """)
        print("\n[UPDATE] Updated S01 level to Intermediate.")

        # Delete
        session.run("""
            MATCH (s:Student {id: "S07"})
            DETACH DELETE s
        """)
        print("\n[DELETE] Detached and deleted student S07.")

    driver.close()

if __name__ == "__main__":
    run_crud()