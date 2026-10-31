// CREATE: Add a new student and enroll them in a course
CREATE (s:Student {id: "S07", name: "Lucas Vance", level: "Beginner"})
WITH s
MATCH (c:Course {code: "CS101"})
CREATE (s)-[:ENROLLED_IN {enrolledOn: "2026-09-01"}]->(c)
RETURN s, c;

// READ 1: Find all students who built a project using 'Cypher'
MATCH (s:Student)-[:BUILT]->(p:Project)-[:USES]->(sk:Skill {name: "Cypher"})
RETURN s.name AS Student, p.name AS Project, sk.name AS Skill;

// READ 2: Mentors teaching courses and skills
MATCH (m:Mentor)-[:TEACHES]->(c:Course)-[:TEACHES_SKILL]->(sk:Skill)
RETURN m.name AS Mentor, c.code AS Course, sk.name AS Skill;

// READ 3: Students interested in target companies
MATCH (s:Student)-[:INTERESTED_IN]->(co:Company)
RETURN s.name AS Student, co.name AS Company;

// UPDATE: Promote student S01 from 'Beginner' to 'Intermediate'
MATCH (s:Student {id: "S01"})
SET s.level = "Intermediate", s.updatedAt = datetime()
RETURN s.id, s.name, s.level, s.updatedAt;

// DELETE: Remove student S07 and any associated relationships safely
MATCH (s:Student {id: "S07"})
DETACH DELETE s;
