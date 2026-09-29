"""
Parameterized CRUD Operations for Job & Skill Knowledge Graph.
Implements Create, Read, Update, and Delete operations for nodes and relationships.
"""
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.connection import Neo4jConnection


# ==========================================
# 1. CREATE OPERATIONS
# ==========================================
def create_candidate(
    conn: Neo4jConnection,
    candidate_id: str,
    name: str,
    experience_yrs: int,
    location: str,
    email: str
) -> Dict[str, Any]:
    """Creates a new Candidate node using parameterized MERGE."""
    cypher = """
    MERGE (c:Candidate {id: $id})
    ON CREATE SET c.name = $name, c.experience_yrs = $experience_yrs, c.location = $location, c.email = $email, c.created_at = datetime()
    ON MATCH SET c.name = $name, c.experience_yrs = $experience_yrs, c.location = $location, c.email = $email, c.updated_at = datetime()
    RETURN { id: c.id, name: c.name, experience_yrs: c.experience_yrs, location: c.location, email: c.email } AS candidate
    """
    params = {
        "id": candidate_id,
        "name": name,
        "experience_yrs": experience_yrs,
        "location": location,
        "email": email,
    }
    result = conn.execute_write(cypher, params)
    return result[0]["candidate"] if result else {}


def add_candidate_skill(
    conn: Neo4jConnection,
    candidate_id: str,
    skill_id: str,
    proficiency: str = "Intermediate",
    years: int = 1
) -> Dict[str, Any]:
    """Links a Candidate to a Skill via HAS_SKILL relationship with properties."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})
    MATCH (s:Skill {id: $skill_id})
    MERGE (c)-[r:HAS_SKILL]->(s)
    SET r.proficiency = $proficiency, r.years = $years
    RETURN c.name AS candidate, s.name AS skill, r.proficiency AS proficiency, r.years AS years
    """
    params = {
        "candidate_id": candidate_id,
        "skill_id": skill_id,
        "proficiency": proficiency,
        "years": years,
    }
    result = conn.execute_write(cypher, params)
    return result[0] if result else {}


# ==========================================
# 2. READ OPERATIONS
# ==========================================
def get_candidate_by_id(conn: Neo4jConnection, candidate_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves candidate details along with their skills, certifications, and applications."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})
    OPTIONAL MATCH (c)-[hs:HAS_SKILL]->(s:Skill)
    OPTIONAL MATCH (c)-[e:EARNED]->(crt:Certification)
    OPTIONAL MATCH (c)-[a:APPLIED_TO]->(j:JobRole)-[:POSTED_BY]->(co:Company)
    WITH c,
         collect(DISTINCT CASE WHEN s IS NOT NULL THEN {id: s.id, name: s.name, category: s.category, proficiency: hs.proficiency, years: hs.years} END) AS skills,
         collect(DISTINCT CASE WHEN crt IS NOT NULL THEN {id: crt.id, title: crt.title, issuer: crt.issuer, earned_date: e.earned_date} END) AS certs,
         collect(DISTINCT CASE WHEN j IS NOT NULL THEN {job_id: j.id, title: j.title, company: co.name, status: a.status, applied_date: a.applied_date} END) AS apps
    RETURN {
        id: c.id,
        name: c.name,
        experience_yrs: c.experience_yrs,
        location: c.location,
        email: c.email,
        skills: [x IN skills WHERE x IS NOT NULL],
        certifications: [x IN certs WHERE x IS NOT NULL],
        applications: [x IN apps WHERE x IS NOT NULL]
    } AS profile
    """
    result = conn.query(cypher, {"candidate_id": candidate_id})
    return result[0]["profile"] if (result and result[0]["profile"]["id"] is not None) else None


def get_job_role_by_id(conn: Neo4jConnection, job_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves JobRole details including company and required skills."""
    cypher = """
    MATCH (j:JobRole {id: $job_id})-[:POSTED_BY]->(co:Company)
    OPTIONAL MATCH (j)-[r:REQUIRES_SKILL]->(s:Skill)
    WITH j, co, collect(DISTINCT CASE WHEN s IS NOT NULL THEN {id: s.id, name: s.name, level: r.level} END) AS req_skills
    RETURN {
        id: j.id,
        title: j.title,
        min_experience: j.min_experience,
        salary_range: j.salary_range,
        location: j.location,
        company: co.name,
        required_skills: [x IN req_skills WHERE x IS NOT NULL]
    } AS job_detail
    """
    result = conn.query(cypher, {"job_id": job_id})
    return result[0]["job_detail"] if (result and result[0]["job_detail"]["id"] is not None) else None


# ==========================================
# 3. UPDATE OPERATIONS
# ==========================================
def update_candidate_experience(conn: Neo4jConnection, candidate_id: str, new_experience: int) -> Dict[str, Any]:
    """Updates candidate years of experience."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})
    SET c.experience_yrs = $new_experience, c.updated_at = datetime()
    RETURN { id: c.id, name: c.name, experience_yrs: c.experience_yrs, location: c.location } AS candidate
    """
    params = {"candidate_id": candidate_id, "new_experience": new_experience}
    result = conn.execute_write(cypher, params)
    return result[0]["candidate"] if result else {}


def update_application_status(conn: Neo4jConnection, candidate_id: str, job_id: str, new_status: str) -> Dict[str, Any]:
    """Updates the status of a job application relationship."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})-[r:APPLIED_TO]->(j:JobRole {id: $job_id})
    SET r.status = $new_status, r.updated_at = datetime()
    RETURN c.name AS candidate, j.title AS job_title, r.status AS new_status
    """
    params = {"candidate_id": candidate_id, "job_id": job_id, "new_status": new_status}
    result = conn.execute_write(cypher, params)
    return result[0] if result else {}


# ==========================================
# 4. DELETE OPERATIONS
# ==========================================
def remove_candidate_skill(conn: Neo4jConnection, candidate_id: str, skill_id: str) -> bool:
    """Deletes HAS_SKILL relationship between a Candidate and a Skill."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})-[r:HAS_SKILL]->(s:Skill {id: $skill_id})
    DELETE r
    RETURN count(r) AS deleted_count
    """
    params = {"candidate_id": candidate_id, "skill_id": skill_id}
    result = conn.execute_write(cypher, params)
    return result[0]["deleted_count"] > 0 if result else False


def delete_candidate(conn: Neo4jConnection, candidate_id: str) -> bool:
    """Detaches and deletes a candidate node along with all attached relationships."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})
    DETACH DELETE c
    RETURN count(c) AS deleted_count
    """
    result = conn.execute_write(cypher, {"candidate_id": candidate_id})
    return result[0]["deleted_count"] > 0 if result else False


if __name__ == "__main__":
    conn = Neo4jConnection()
    try:
        print("--- Testing CRUD Operations ---")
        # Test Create
        temp_c = create_candidate(conn, "C999", "Test User", 5, "Austin, TX", "test.user@example.com")
        print("Created Candidate:", temp_c)

        # Test Read
        profile = get_candidate_by_id(conn, "C999")
        print("Read Profile:", profile["name"] if profile else "Not Found")

        # Test Update
        updated = update_candidate_experience(conn, "C999", 6)
        print("Updated Experience:", updated.get("experience_yrs"))

        # Test Delete
        deleted = delete_candidate(conn, "C999")
        print("Deleted Successfully:", deleted)
    finally:
        conn.close()
