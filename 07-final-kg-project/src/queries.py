"""
Analytical Cypher Queries Module for Neo4j Knowledge Graph.
Contains 10+ Multi-hop traversals, parameterized recommendations, skill-gap analysis, and graph analytics.
"""
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.connection import Neo4jConnection


# -------------------------------------------------------------------------
# Query 1: Candidate Profile & Skill Verification (1-Hop / Multi-Branch)
# -------------------------------------------------------------------------
def q1_candidate_skills_and_certs(conn: Neo4jConnection, candidate_id: str = "C01") -> List[Dict[str, Any]]:
    """Query 1: Fetch candidate profile, skills with proficiency, and verified certifications."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})
    OPTIONAL MATCH (c)-[hs:HAS_SKILL]->(s:Skill)
    OPTIONAL MATCH (c)-[e:EARNED]->(crt:Certification)
    RETURN c.name AS Candidate,
           c.experience_yrs AS ExperienceYears,
           collect(DISTINCT s.name + ' (' + hs.proficiency + ')') AS Skills,
           collect(DISTINCT crt.title) AS Certifications
    """
    return conn.query(cypher, {"candidate_id": candidate_id})


# -------------------------------------------------------------------------
# Query 2: Direct Job Role Skill Match (2-Hop Traversal)
# -------------------------------------------------------------------------
def q2_candidate_job_matches(conn: Neo4jConnection, candidate_id: str = "C01") -> List[Dict[str, Any]]:
    """Query 2: Find job roles matching a candidate's skills and compute match percentage."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})-[hs:HAS_SKILL]->(s:Skill)
    MATCH (j:JobRole)-[r:REQUIRES_SKILL]->(s)
    MATCH (j)-[:POSTED_BY]->(co:Company)
    WITH c, j, co, count(s) AS matched_skills_count
    MATCH (j)-[:REQUIRES_SKILL]->(total_s:Skill)
    WITH c, j, co, matched_skills_count, count(total_s) AS total_required_skills
    WHERE c.experience_yrs >= j.min_experience
    RETURN j.id AS JobID,
           j.title AS JobTitle,
           co.name AS Company,
           j.salary_range AS Salary,
           matched_skills_count AS MatchedSkills,
           total_required_skills AS TotalRequiredSkills,
           round(100.0 * matched_skills_count / total_required_skills, 1) AS MatchPercentage
    ORDER BY MatchPercentage DESC, MatchedSkills DESC
    """
    return conn.query(cypher, {"candidate_id": candidate_id})


# -------------------------------------------------------------------------
# Query 3: Multi-Hop Skill Gap Analysis for Target Job Role (2-Hop)
# -------------------------------------------------------------------------
def q3_skill_gap_analysis(conn: Neo4jConnection, candidate_id: str = "C01", job_id: str = "J02") -> List[Dict[str, Any]]:
    """Query 3: Identify missing mandatory and preferred skills for a candidate targeting a specific job."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})
    MATCH (j:JobRole {id: $job_id})-[:POSTED_BY]->(co:Company)
    MATCH (j)-[r:REQUIRES_SKILL]->(s:Skill)
    WHERE NOT (c)-[:HAS_SKILL]->(s)
    RETURN c.name AS Candidate,
           j.title AS TargetJob,
           co.name AS TargetCompany,
           s.name AS MissingSkill,
           s.category AS SkillCategory,
           r.level AS RequirementLevel
    ORDER BY r.level DESC, s.name ASC
    """
    return conn.query(cypher, {"candidate_id": candidate_id, "job_id": job_id})


# -------------------------------------------------------------------------
# Query 4: Learning Path Recommendation (3-Hop Traversal)
# -------------------------------------------------------------------------
def q4_learning_path_recommendations(conn: Neo4jConnection, candidate_id: str = "C01", job_id: str = "J02") -> List[Dict[str, Any]]:
    """Query 4: 3-Hop Traversal recommending courses & certifications to fill candidate skill gaps for a target job."""
    cypher = """
    MATCH (c:Candidate {id: $candidate_id})
    MATCH (j:JobRole {id: $job_id})-[:REQUIRES_SKILL]->(s:Skill)
    WHERE NOT (c)-[:HAS_SKILL]->(s)
    OPTIONAL MATCH (crs:Course)-[:TEACHES]->(s)
    OPTIONAL MATCH (crt:Certification)-[:VALIDATES]->(s)
    RETURN s.name AS MissingSkill,
           collect(DISTINCT crs.title + ' [' + crs.platform + ', ' + toString(crs.duration_hours) + 'h]') AS RecommendedCourses,
           collect(DISTINCT crt.title + ' [Issuer: ' + crt.issuer + ']') AS RecommendedCertifications
    ORDER BY MissingSkill ASC
    """
    return conn.query(cypher, {"candidate_id": candidate_id, "job_id": job_id})


# -------------------------------------------------------------------------
# Query 5: Top Demanded Skills Aggregation
# -------------------------------------------------------------------------
def q5_top_demanded_skills(conn: Neo4jConnection, limit: int = 5) -> List[Dict[str, Any]]:
    """Query 5: Find the top demanded skills across all active job postings."""
    cypher = """
    MATCH (s:Skill)<-[r:REQUIRES_SKILL]-(j:JobRole)
    RETURN s.id AS SkillID,
           s.name AS SkillName,
           s.category AS Category,
           count(j) AS TotalJobsRequesting,
           sum(CASE WHEN r.level = 'Mandatory' THEN 1 ELSE 0 END) AS MandatoryCount,
           sum(CASE WHEN r.level = 'Preferred' THEN 1 ELSE 0 END) AS PreferredCount
    ORDER BY TotalJobsRequesting DESC, MandatoryCount DESC
    LIMIT $limit
    """
    return conn.query(cypher, {"limit": limit})


# -------------------------------------------------------------------------
# Query 6: Company Tech Stack Discovery (Multi-Hop Traversal)
# -------------------------------------------------------------------------
def q6_company_tech_stack(conn: Neo4jConnection, company_id: str = "CO01") -> List[Dict[str, Any]]:
    """Query 6: Discover full technology stack required by open roles in a specific company."""
    cypher = """
    MATCH (co:Company {id: $company_id})<-[:POSTED_BY]-(j:JobRole)-[r:REQUIRES_SKILL]->(s:Skill)
    RETURN co.name AS CompanyName,
           s.category AS SkillCategory,
           collect(DISTINCT s.name) AS Technologies,
           count(DISTINCT j) AS RequiredInNumJobs
    ORDER BY RequiredInNumJobs DESC, SkillCategory ASC
    """
    return conn.query(cypher, {"company_id": company_id})


# -------------------------------------------------------------------------
# Query 7: Candidate Peer Network & Skill Overlap (3-Hop Peer Search)
# -------------------------------------------------------------------------
def q7_candidate_peer_proximity(conn: Neo4jConnection, candidate_id: str = "C01") -> List[Dict[str, Any]]:
    """Query 7: Find peer candidates with highest skill overlap for collaboration or talent matching."""
    cypher = """
    MATCH (c1:Candidate {id: $candidate_id})-[hs1:HAS_SKILL]->(s:Skill)<-[hs2:HAS_SKILL]-(c2:Candidate)
    WHERE c1 <> c2
    WITH c1, c2, collect(s.name) AS CommonSkills, count(s) AS SharedSkillCount
    MATCH (c1)-[:HAS_SKILL]->(all_s1:Skill)
    WITH c1, c2, CommonSkills, SharedSkillCount, count(all_s1) AS C1SkillCount
    RETURN c2.id AS PeerID,
           c2.name AS PeerName,
           c2.location AS Location,
           c2.experience_yrs AS ExperienceYears,
           SharedSkillCount,
           CommonSkills,
           round(100.0 * SharedSkillCount / C1SkillCount, 1) AS OverlapPercentage
    ORDER BY SharedSkillCount DESC, OverlapPercentage DESC
    LIMIT 5
    """
    return conn.query(cypher, {"candidate_id": candidate_id})


# -------------------------------------------------------------------------
# Query 8: Talent Pipeline - Top Candidates for a Job Role (Multi-Hop Ranking)
# -------------------------------------------------------------------------
def q8_top_candidates_for_job(conn: Neo4jConnection, job_id: str = "J01") -> List[Dict[str, Any]]:
    """Query 8: Rank candidates for a target job based on mandatory skill coverage and experience."""
    cypher = """
    MATCH (j:JobRole {id: $job_id})-[:REQUIRES_SKILL {level: 'Mandatory'}]->(s:Skill)
    WITH j, collect(s) AS mandatory_skills, count(s) AS mandatory_count
    MATCH (c:Candidate)-[hs:HAS_SKILL]->(s:Skill) WHERE s IN mandatory_skills
    WITH j, c, mandatory_count, count(s) AS candidate_mandatory_matches, collect(s.name) AS matched_skills
    WHERE c.experience_yrs >= j.min_experience
    RETURN c.id AS CandidateID,
           c.name AS CandidateName,
           c.experience_yrs AS Experience,
           candidate_mandatory_matches AS MandatoryMatches,
           mandatory_count AS TotalMandatoryRequired,
           matched_skills AS SkillsPossessed,
           round(100.0 * candidate_mandatory_matches / mandatory_count, 1) AS MandatoryCoverage
    ORDER BY MandatoryCoverage DESC, c.experience_yrs DESC
    """
    return conn.query(cypher, {"job_id": job_id})


# -------------------------------------------------------------------------
# Query 9: Certification Market Value Metric (Multi-Hop Aggregation)
# -------------------------------------------------------------------------
def q9_certification_value_metric(conn: Neo4jConnection) -> List[Dict[str, Any]]:
    """Query 9: Rank certifications by market demand of skills they validate and candidate adoption."""
    cypher = """
    MATCH (crt:Certification)-[:VALIDATES]->(s:Skill)
    OPTIONAL MATCH (s)<-[:REQUIRES_SKILL]-(j:JobRole)
    OPTIONAL MATCH (crt)<-[:EARNED]-(c:Candidate)
    RETURN crt.id AS CertID,
           crt.title AS CertificationTitle,
           crt.issuer AS Issuer,
           collect(DISTINCT s.name) AS ValidatedSkills,
           count(DISTINCT j) AS AssociatedJobRolesCount,
           count(DISTINCT c) AS TotalCertifiedCandidates
    ORDER BY AssociatedJobRolesCount DESC, TotalCertifiedCandidates DESC
    """
    return conn.query(cypher)


# -------------------------------------------------------------------------
# Query 10: Candidate Application Status Tracker (Multi-Hop Pipeline)
# -------------------------------------------------------------------------
def q10_application_status_tracker(conn: Neo4jConnection, status: str = "Interviewing") -> List[Dict[str, Any]]:
    """Query 10: Track applicants across companies filtered by application status."""
    cypher = """
    MATCH (c:Candidate)-[a:APPLIED_TO]->(j:JobRole)-[:POSTED_BY]->(co:Company)
    WHERE a.status = $status
    RETURN c.id AS CandidateID,
           c.name AS CandidateName,
           j.title AS AppliedJobTitle,
           co.name AS CompanyName,
           a.applied_date AS AppliedDate,
           a.status AS ApplicationStatus
    ORDER BY a.applied_date DESC
    """
    return conn.query(cypher, {"status": status})


# -------------------------------------------------------------------------
# Query 11: Learning Hub - Course Platforms for In-Demand Skills (Bonus Multi-Hop)
# -------------------------------------------------------------------------
def q11_course_platforms_for_demand(conn: Neo4jConnection) -> List[Dict[str, Any]]:
    """Query 11: Aggregates courses and platforms teaching high-demand skills."""
    cypher = """
    MATCH (crs:Course)-[:TEACHES]->(s:Skill)<-[:REQUIRES_SKILL]-(j:JobRole)
    RETURN crs.platform AS Platform,
           count(DISTINCT crs) AS CourseCount,
           collect(DISTINCT s.name) AS SkillsTaught,
           count(DISTINCT j) AS MarketJobDemand
    ORDER BY MarketJobDemand DESC
    """
    return conn.query(cypher)


def run_all_queries(conn: Neo4jConnection):
    """Executes and displays output for all 10+ Cypher queries."""
    from tabulate import tabulate

    queries_list = [
        ("1. Candidate Skills & Certifications Lookup (C01)", lambda: q1_candidate_skills_and_certs(conn, "C01")),
        ("2. Candidate Job Matches (C01)", lambda: q2_candidate_job_matches(conn, "C01")),
        ("3. Skill Gap Analysis (C01 for Job J02)", lambda: q3_skill_gap_analysis(conn, "C01", "J02")),
        ("4. Learning Path Recommendations (3-Hop)", lambda: q4_learning_path_recommendations(conn, "C01", "J02")),
        ("5. Top 5 Most Demanded Skills", lambda: q5_top_demanded_skills(conn, 5)),
        ("6. Company Tech Stack Discovery (CO01)", lambda: q6_company_tech_stack(conn, "CO01")),
        ("7. Candidate Peer Proximity (C01 Overlap)", lambda: q7_candidate_peer_proximity(conn, "C01")),
        ("8. Top Candidates for Job (J01)", lambda: q8_top_candidates_for_job(conn, "J01")),
        ("9. Certification Market Value Metric", lambda: q9_certification_value_metric(conn)),
        ("10. Application Status Tracker (Interviewing)", lambda: q10_application_status_tracker(conn, "Interviewing")),
        ("11. Course Platforms for In-Demand Skills", lambda: q11_course_platforms_for_demand(conn)),
    ]

    for title, query_fn in queries_list:
        print(f"\n=======================================================")
        print(f" {title}")
        print(f"=======================================================")
        res = query_fn()
        if res:
            print(tabulate(res, headers="keys", tablefmt="grid"))
        else:
            print("No records returned.")


if __name__ == "__main__":
    conn = Neo4jConnection()
    try:
        run_all_queries(conn)
    finally:
        conn.close()
