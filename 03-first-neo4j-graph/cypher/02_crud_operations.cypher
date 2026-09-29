// CREATE: Add a new student and enroll them in a course
CREATE (s:Student {id: "S07", name: "Lucas Vance", level: "Beginner"})
WITH s
MATCH (c:Course {code: "CS101"})
CREATE (s)-[:ENROLLED_IN {enrolledOn: "2026-09-01"}]->(c)
RETURN s, c;

// READ: Find all students who built a project using 'Cypher'
MATCH (s:Student)-[:BUILT]->(p:Project)-[:USES]->(sk:Skill {name: "Cypher"})
RETURN s.name AS Student, p.name AS Project, sk.name AS Skill;

// UPDATE: Promote student S01 from 'Beginner' to 'Intermediate'
MATCH (s:Student {id: "S01"})
SET s.level = "Intermediate", s.updatedAt = datetime()
RETURN s.id, s.name, s.level;

// DELETE: Remove student S07 and any associated relationships safely
MATCH (s:Student {id: "S07"})
DETACH DELETE s;