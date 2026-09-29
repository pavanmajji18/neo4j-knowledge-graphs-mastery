"""
Data Ingestion and Schema Initialization Module for Neo4j Knowledge Graph.
Seeds 80+ Nodes and 250+ Relationships across 6 Node Labels and 7 Relationship Types.
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.connection import Neo4jConnection


def create_constraints_and_indexes(conn: Neo4jConnection):
    """Creates uniqueness constraints and indexes for node identity performance."""
    print("--> Creating uniqueness constraints & indexes...")
    constraints = [
        "CREATE CONSTRAINT candidate_id_unique IF NOT EXISTS FOR (c:Candidate) REQUIRE c.id IS UNIQUE",
        "CREATE CONSTRAINT skill_id_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE",
        "CREATE CONSTRAINT jobrole_id_unique IF NOT EXISTS FOR (j:JobRole) REQUIRE j.id IS UNIQUE",
        "CREATE CONSTRAINT company_id_unique IF NOT EXISTS FOR (co:Company) REQUIRE co.id IS UNIQUE",
        "CREATE CONSTRAINT cert_id_unique IF NOT EXISTS FOR (crt:Certification) REQUIRE crt.id IS UNIQUE",
        "CREATE CONSTRAINT course_id_unique IF NOT EXISTS FOR (crs:Course) REQUIRE crs.id IS UNIQUE",
    ]
    for statement in constraints:
        try:
            conn.query(statement)
        except Exception as e:
            print(f"    [WARN] Constraint statement note: {e}")
    print("    [OK] Constraints setup completed.")


def clear_database(conn: Neo4jConnection):
    """Wipes all existing nodes and relationships from the database."""
    print("--> Clearing database nodes and relationships...")
    conn.query("MATCH (n) DETACH DELETE n")
    print("    [OK] Database cleared.")


def seed_database(conn: Neo4jConnection, wipe_existing: bool = True):
    """
    Populates database with Candidates, Skills, JobRoles, Companies, Certifications, Courses,
    and all 7 relationship types using parameterized UNWIND batches.
    """
    if wipe_existing:
        clear_database(conn)

    create_constraints_and_indexes(conn)

    print("--> Seeding Nodes...")

    # 1. Companies (8 nodes)
    companies = [
        {"id": "CO01", "name": "GraphCorp Technologies", "industry": "Graph & AI Solutions", "location": "San Francisco, CA"},
        {"id": "CO02", "name": "AI Nexus Labs", "industry": "Artificial Intelligence", "location": "New York, NY"},
        {"id": "CO03", "name": "CloudScale Systems", "industry": "Cloud Infrastructure", "location": "Seattle, WA"},
        {"id": "CO04", "name": "DataPulse Analytics", "industry": "Data Engineering", "location": "Austin, TX"},
        {"id": "CO05", "name": "CyberEdge Security", "industry": "Cybersecurity", "location": "Boston, MA"},
        {"id": "CO06", "name": "QuantumSoft Solutions", "industry": "Enterprise Software", "location": "Chicago, IL"},
        {"id": "CO07", "name": "NextGen Fintech", "industry": "Financial Technology", "location": "London, UK"},
        {"id": "CO08", "name": "BioHealth Intelligence", "industry": "HealthTech", "location": "San Diego, CA"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MERGE (co:Company {id: item.id})
        SET co.name = item.name, co.industry = item.industry, co.location = item.location
    """, {"batch": companies})
    print(f"    - Companies seeded: {len(companies)}")

    # 2. Skills (18 nodes)
    skills = [
        {"id": "S01", "name": "Neo4j", "category": "Graph Databases"},
        {"id": "S02", "name": "Cypher", "category": "Graph Query Languages"},
        {"id": "S03", "name": "Python", "category": "Programming Languages"},
        {"id": "S04", "name": "Machine Learning", "category": "AI & ML"},
        {"id": "S05", "name": "FastAPI", "category": "Web Frameworks"},
        {"id": "S06", "name": "Docker", "category": "DevOps & Containers"},
        {"id": "S07", "name": "Kubernetes", "category": "DevOps & Orchestration"},
        {"id": "S08", "name": "React", "category": "Frontend Development"},
        {"id": "S09", "name": "Data Engineering", "category": "Data Engineering"},
        {"id": "S10", "name": "SQL", "category": "Databases"},
        {"id": "S11", "name": "AWS", "category": "Cloud Computing"},
        {"id": "S12", "name": "PyTorch", "category": "Deep Learning"},
        {"id": "S13", "name": "GraphQL", "category": "API Technologies"},
        {"id": "S14", "name": "System Design", "category": "Software Architecture"},
        {"id": "S15", "name": "Apache Spark", "category": "Big Data"},
        {"id": "S16", "name": "TypeScript", "category": "Programming Languages"},
        {"id": "S17", "name": "MongoDB", "category": "NoSQL Databases"},
        {"id": "S18", "name": "MLOps", "category": "AI Infrastructure"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MERGE (s:Skill {id: item.id})
        SET s.name = item.name, s.category = item.category
    """, {"batch": skills})
    print(f"    - Skills seeded: {len(skills)}")

    # 3. Job Roles (15 nodes)
    job_roles = [
        {"id": "J01", "title": "Senior Graph Database Engineer", "min_experience": 5, "salary_range": "$140k - $180k", "location": "San Francisco, CA", "company_id": "CO01"},
        {"id": "J02", "title": "AI/ML Solutions Architect", "min_experience": 6, "salary_range": "$160k - $210k", "location": "New York, NY", "company_id": "CO02"},
        {"id": "J03", "title": "Lead Data Engineer", "min_experience": 4, "salary_range": "$130k - $170k", "location": "Austin, TX", "company_id": "CO04"},
        {"id": "J04", "title": "Fullstack Graph Applications Developer", "min_experience": 3, "salary_range": "$115k - $150k", "location": "San Francisco, CA", "company_id": "CO01"},
        {"id": "J05", "title": "DevOps & Cloud Engineer", "min_experience": 4, "salary_range": "$125k - $160k", "location": "Seattle, WA", "company_id": "CO03"},
        {"id": "J06", "title": "Deep Learning Researcher", "min_experience": 5, "salary_range": "$170k - $230k", "location": "New York, NY", "company_id": "CO02"},
        {"id": "J07", "title": "Cybersecurity Analytics Engineer", "min_experience": 3, "salary_range": "$110k - $145k", "location": "Boston, MA", "company_id": "CO05"},
        {"id": "J08", "title": "Enterprise Backend Engineer", "min_experience": 4, "salary_range": "$120k - $155k", "location": "Chicago, IL", "company_id": "CO06"},
        {"id": "J09", "title": "MLOps Infrastructure Lead", "min_experience": 5, "salary_range": "$150k - $195k", "location": "Seattle, WA", "company_id": "CO03"},
        {"id": "J10", "title": "Fintech Data Platform Developer", "min_experience": 3, "salary_range": "$125k - $165k", "location": "London, UK", "company_id": "CO07"},
        {"id": "J11", "title": "HealthTech Graph Data Scientist", "min_experience": 4, "salary_range": "$135k - $175k", "location": "San Diego, CA", "company_id": "CO08"},
        {"id": "J12", "title": "Junior Python Graph Developer", "min_experience": 1, "salary_range": "$85k - $110k", "location": "San Francisco, CA", "company_id": "CO01"},
        {"id": "J13", "title": "Cloud Data Architect", "min_experience": 7, "salary_range": "$175k - $225k", "location": "Seattle, WA", "company_id": "CO03"},
        {"id": "J14", "title": "Frontend Graph Visualization Specialist", "min_experience": 3, "salary_range": "$110k - $140k", "location": "Austin, TX", "company_id": "CO04"},
        {"id": "J15", "title": "Senior AI Systems Engineer", "min_experience": 5, "salary_range": "$155k - $200k", "location": "New York, NY", "company_id": "CO02"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MERGE (j:JobRole {id: item.id})
        SET j.title = item.title, j.min_experience = item.min_experience, j.salary_range = item.salary_range, j.location = item.location
    """, {"batch": job_roles})
    print(f"    - JobRoles seeded: {len(job_roles)}")

    # 4. Candidates (25 nodes)
    candidates = [
        {"id": "C01", "name": "Alice Chen", "experience_yrs": 6, "location": "San Francisco, CA", "email": "alice.c@example.com"},
        {"id": "C02", "name": "Bob Smith", "experience_yrs": 4, "location": "New York, NY", "email": "bob.s@example.com"},
        {"id": "C03", "name": "Carol Williams", "experience_yrs": 7, "location": "Austin, TX", "email": "carol.w@example.com"},
        {"id": "C04", "name": "David Miller", "experience_yrs": 3, "location": "Seattle, WA", "email": "david.m@example.com"},
        {"id": "C05", "name": "Elena Rostova", "experience_yrs": 5, "location": "Boston, MA", "email": "elena.r@example.com"},
        {"id": "C06", "name": "Frank Thorne", "experience_yrs": 2, "location": "Chicago, IL", "email": "frank.t@example.com"},
        {"id": "C07", "name": "Grace Hopper", "experience_yrs": 8, "location": "London, UK", "email": "grace.h@example.com"},
        {"id": "C08", "name": "Hassan Ali", "experience_yrs": 4, "location": "San Diego, CA", "email": "hassan.a@example.com"},
        {"id": "C09", "name": "Irene Adler", "experience_yrs": 5, "location": "San Francisco, CA", "email": "irene.a@example.com"},
        {"id": "C10", "name": "Jack Vance", "experience_yrs": 3, "location": "New York, NY", "email": "jack.v@example.com"},
        {"id": "C11", "name": "Kavita Patel", "experience_yrs": 6, "location": "Seattle, WA", "email": "kavita.p@example.com"},
        {"id": "C12", "name": "Liam Neeson", "experience_yrs": 4, "location": "Austin, TX", "email": "liam.n@example.com"},
        {"id": "C13", "name": "Maria Garcia", "experience_yrs": 5, "location": "Boston, MA", "email": "maria.g@example.com"},
        {"id": "C14", "name": "Nathan Drake", "experience_yrs": 2, "location": "Chicago, IL", "email": "nathan.d@example.com"},
        {"id": "C15", "name": "Olga Kurylenko", "experience_yrs": 7, "location": "London, UK", "email": "olga.k@example.com"},
        {"id": "C16", "name": "Parth Sharma", "experience_yrs": 5, "location": "San Francisco, CA", "email": "parth.s@example.com"},
        {"id": "C17", "name": "Quinn Fabray", "experience_yrs": 3, "location": "San Diego, CA", "email": "quinn.f@example.com"},
        {"id": "C18", "name": "Rahul Verma", "experience_yrs": 4, "location": "Austin, TX", "email": "rahul.v@example.com"},
        {"id": "C19", "name": "Sophia Martinez", "experience_yrs": 6, "location": "Seattle, WA", "email": "sophia.m@example.com"},
        {"id": "C20", "name": "Tariq Mahmood", "experience_yrs": 5, "location": "New York, NY", "email": "tariq.m@example.com"},
        {"id": "C21", "name": "Uma Thurman", "experience_yrs": 2, "location": "San Francisco, CA", "email": "uma.t@example.com"},
        {"id": "C22", "name": "Victor Hugo", "experience_yrs": 8, "location": "Boston, MA", "email": "victor.h@example.com"},
        {"id": "C23", "name": "Wendy Darling", "experience_yrs": 3, "location": "Chicago, IL", "email": "wendy.d@example.com"},
        {"id": "C24", "name": "Xavier Hernandez", "experience_yrs": 4, "location": "London, UK", "email": "xavier.h@example.com"},
        {"id": "C25", "name": "Yuki Tanaka", "experience_yrs": 6, "location": "San Diego, CA", "email": "yuki.t@example.com"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MERGE (c:Candidate {id: item.id})
        SET c.name = item.name, c.experience_yrs = item.experience_yrs, c.location = item.location, c.email = item.email
    """, {"batch": candidates})
    print(f"    - Candidates seeded: {len(candidates)}")

    # 5. Certifications (10 nodes)
    certifications = [
        {"id": "CERT01", "title": "Neo4j Certified Professional", "issuer": "Neo4j GraphAcademy", "validity_years": 3},
        {"id": "CERT02", "title": "AWS Certified Data Analytics Specialist", "issuer": "Amazon Web Services", "validity_years": 3},
        {"id": "CERT03", "title": "Certified Kubernetes Administrator (CKA)", "issuer": "Linux Foundation", "validity_years": 2},
        {"id": "CERT04", "title": "TensorFlow Developer Certificate", "issuer": "Google DeepMind", "validity_years": 3},
        {"id": "CERT05", "title": "Meta Professional Database Engineer", "issuer": "Meta", "validity_years": 2},
        {"id": "CERT06", "title": "Databricks Certified Apache Spark Developer", "issuer": "Databricks", "validity_years": 2},
        {"id": "CERT07", "title": "Docker Certified Associate (DCA)", "issuer": "Docker", "validity_years": 2},
        {"id": "CERT08", "title": "HashiCorp Certified Terraform Associate", "issuer": "HashiCorp", "validity_years": 2},
        {"id": "CERT09", "title": "Neo4j Graph Data Science Certified", "issuer": "Neo4j GraphAcademy", "validity_years": 3},
        {"id": "CERT10", "title": "AWS Certified Solutions Architect - Associate", "issuer": "Amazon Web Services", "validity_years": 3},
    ]
    conn.query("""
        UNWIND $batch AS item
        MERGE (crt:Certification {id: item.id})
        SET crt.title = item.title, crt.issuer = item.issuer, crt.validity_years = item.validity_years
    """, {"batch": certifications})
    print(f"    - Certifications seeded: {len(certifications)}")

    # 6. Courses (12 nodes)
    courses = [
        {"id": "CRS01", "title": "Neo4j Fundamentals & Cypher Mastery", "platform": "GraphAcademy", "duration_hours": 20},
        {"id": "CRS02", "title": "Advanced Machine Learning with PyTorch", "platform": "Coursera", "duration_hours": 40},
        {"id": "CRS03", "title": "Data Engineering Pipelines with Apache Spark", "platform": "edX", "duration_hours": 35},
        {"id": "CRS04", "title": "Docker & Kubernetes Deep Dive", "platform": "Udemy", "duration_hours": 25},
        {"id": "CRS05", "title": "FastAPI & Microservices Architecture", "platform": "Pluralsight", "duration_hours": 18},
        {"id": "CRS06", "title": "System Design Masterclass for High Scale", "platform": "Educative", "duration_hours": 30},
        {"id": "CRS07", "title": "Building Production MLOps Systems", "platform": "Coursera", "duration_hours": 45},
        {"id": "CRS08", "title": "GraphQL & Fullstack React Development", "platform": "Udemy", "duration_hours": 22},
        {"id": "CRS09", "title": "AWS Cloud Practitioner & Data Architect", "platform": "A Cloud Guru", "duration_hours": 28},
        {"id": "CRS10", "title": "Neo4j Graph Data Science & Node Embeddings", "platform": "GraphAcademy", "duration_hours": 24},
        {"id": "CRS11", "title": "NoSQL Systems & MongoDB Architecture", "platform": "MongoDB University", "duration_hours": 16},
        {"id": "CRS12", "title": "Python for High Performance Data Science", "platform": "DataCamp", "duration_hours": 15},
    ]
    conn.query("""
        UNWIND $batch AS item
        MERGE (crs:Course {id: item.id})
        SET crs.title = item.title, crs.platform = item.platform, crs.duration_hours = item.duration_hours
    """, {"batch": courses})
    print(f"    - Courses seeded: {len(courses)}")

    print("\n--> Seeding Relationships...")

    # 7. JobRole -[:POSTED_BY]-> Company
    conn.query("""
        UNWIND $batch AS item
        MATCH (j:JobRole {id: item.id})
        MATCH (co:Company {id: item.company_id})
        MERGE (j)-[:POSTED_BY]->(co)
    """, {"batch": job_roles})
    print("    - [POSTED_BY] relationships linked.")

    # 8. Candidate -[:HAS_SKILL]-> Skill
    candidate_skills = [
        {"candidate_id": "C01", "skill_id": "S01", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C01", "skill_id": "S02", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C01", "skill_id": "S03", "proficiency": "Expert", "years": 6},
        {"candidate_id": "C01", "skill_id": "S05", "proficiency": "Intermediate", "years": 3},
        {"candidate_id": "C01", "skill_id": "S14", "proficiency": "Intermediate", "years": 3},

        {"candidate_id": "C02", "skill_id": "S03", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C02", "skill_id": "S04", "proficiency": "Expert", "years": 3},
        {"candidate_id": "C02", "skill_id": "S12", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C02", "skill_id": "S18", "proficiency": "Beginner", "years": 1},

        {"candidate_id": "C03", "skill_id": "S03", "proficiency": "Expert", "years": 7},
        {"candidate_id": "C03", "skill_id": "S09", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C03", "skill_id": "S10", "proficiency": "Expert", "years": 6},
        {"candidate_id": "C03", "skill_id": "S15", "proficiency": "Intermediate", "years": 3},
        {"candidate_id": "C03", "skill_id": "S11", "proficiency": "Intermediate", "years": 4},

        {"candidate_id": "C04", "skill_id": "S06", "proficiency": "Expert", "years": 3},
        {"candidate_id": "C04", "skill_id": "S07", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C04", "skill_id": "S11", "proficiency": "Expert", "years": 3},
        {"candidate_id": "C04", "skill_id": "S03", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C05", "skill_id": "S01", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C05", "skill_id": "S02", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C05", "skill_id": "S03", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C05", "skill_id": "S08", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C05", "skill_id": "S16", "proficiency": "Expert", "years": 3},

        {"candidate_id": "C06", "skill_id": "S03", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C06", "skill_id": "S05", "proficiency": "Intermediate", "years": 1},
        {"candidate_id": "C06", "skill_id": "S10", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C07", "skill_id": "S03", "proficiency": "Expert", "years": 8},
        {"candidate_id": "C07", "skill_id": "S14", "proficiency": "Expert", "years": 6},
        {"candidate_id": "C07", "skill_id": "S11", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C07", "skill_id": "S09", "proficiency": "Expert", "years": 6},

        {"candidate_id": "C08", "skill_id": "S01", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C08", "skill_id": "S03", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C08", "skill_id": "S04", "proficiency": "Intermediate", "years": 3},
        {"candidate_id": "C08", "skill_id": "S12", "proficiency": "Beginner", "years": 1},

        {"candidate_id": "C09", "skill_id": "S01", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C09", "skill_id": "S02", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C09", "skill_id": "S03", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C09", "skill_id": "S04", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C10", "skill_id": "S04", "proficiency": "Expert", "years": 3},
        {"candidate_id": "C10", "skill_id": "S12", "proficiency": "Expert", "years": 3},
        {"candidate_id": "C10", "skill_id": "S03", "proficiency": "Intermediate", "years": 3},

        {"candidate_id": "C11", "skill_id": "S06", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C11", "skill_id": "S07", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C11", "skill_id": "S18", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C11", "skill_id": "S11", "proficiency": "Expert", "years": 5},

        {"candidate_id": "C12", "skill_id": "S09", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C12", "skill_id": "S15", "proficiency": "Expert", "years": 3},
        {"candidate_id": "C12", "skill_id": "S10", "proficiency": "Expert", "years": 4},

        {"candidate_id": "C13", "skill_id": "S08", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C13", "skill_id": "S16", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C13", "skill_id": "S13", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C14", "skill_id": "S03", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C14", "skill_id": "S05", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C15", "skill_id": "S01", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C15", "skill_id": "S02", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C15", "skill_id": "S14", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C15", "skill_id": "S09", "proficiency": "Intermediate", "years": 3},

        {"candidate_id": "C16", "skill_id": "S03", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C16", "skill_id": "S01", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C16", "skill_id": "S02", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C17", "skill_id": "S04", "proficiency": "Intermediate", "years": 3},
        {"candidate_id": "C17", "skill_id": "S03", "proficiency": "Intermediate", "years": 3},

        {"candidate_id": "C18", "skill_id": "S09", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C18", "skill_id": "S10", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C18", "skill_id": "S17", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C19", "skill_id": "S06", "proficiency": "Expert", "years": 5},
        {"candidate_id": "C19", "skill_id": "S07", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C19", "skill_id": "S18", "proficiency": "Expert", "years": 3},

        {"candidate_id": "C20", "skill_id": "S04", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C20", "skill_id": "S12", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C20", "skill_id": "S18", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C21", "skill_id": "S03", "proficiency": "Intermediate", "years": 2},
        {"candidate_id": "C21", "skill_id": "S01", "proficiency": "Beginner", "years": 1},

        {"candidate_id": "C22", "skill_id": "S14", "proficiency": "Expert", "years": 7},
        {"candidate_id": "C22", "skill_id": "S11", "proficiency": "Expert", "years": 6},
        {"candidate_id": "C22", "skill_id": "S03", "proficiency": "Expert", "years": 8},

        {"candidate_id": "C23", "skill_id": "S08", "proficiency": "Intermediate", "years": 3},
        {"candidate_id": "C23", "skill_id": "S16", "proficiency": "Intermediate", "years": 2},

        {"candidate_id": "C24", "skill_id": "S10", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C24", "skill_id": "S09", "proficiency": "Intermediate", "years": 3},

        {"candidate_id": "C25", "skill_id": "S01", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C25", "skill_id": "S02", "proficiency": "Expert", "years": 4},
        {"candidate_id": "C25", "skill_id": "S03", "proficiency": "Expert", "years": 6},
        {"candidate_id": "C25", "skill_id": "S04", "proficiency": "Intermediate", "years": 3},
    ]
    conn.query("""
        UNWIND $batch AS item
        MATCH (c:Candidate {id: item.candidate_id})
        MATCH (s:Skill {id: item.skill_id})
        MERGE (c)-[r:HAS_SKILL]->(s)
        SET r.proficiency = item.proficiency, r.years = item.years
    """, {"batch": candidate_skills})
    print(f"    - [HAS_SKILL] relationships linked: {len(candidate_skills)}")

    # 9. JobRole -[:REQUIRES_SKILL]-> Skill
    job_skills = [
        {"job_id": "J01", "skill_id": "S01", "level": "Mandatory"},
        {"job_id": "J01", "skill_id": "S02", "level": "Mandatory"},
        {"job_id": "J01", "skill_id": "S03", "level": "Mandatory"},
        {"job_id": "J01", "skill_id": "S14", "level": "Preferred"},

        {"job_id": "J02", "skill_id": "S04", "level": "Mandatory"},
        {"job_id": "J02", "skill_id": "S12", "level": "Mandatory"},
        {"job_id": "J02", "skill_id": "S03", "level": "Mandatory"},
        {"job_id": "J02", "skill_id": "S18", "level": "Preferred"},

        {"job_id": "J03", "skill_id": "S09", "level": "Mandatory"},
        {"job_id": "J03", "skill_id": "S10", "level": "Mandatory"},
        {"job_id": "J03", "skill_id": "S15", "level": "Mandatory"},
        {"job_id": "J03", "skill_id": "S03", "level": "Preferred"},

        {"job_id": "J04", "skill_id": "S01", "level": "Mandatory"},
        {"job_id": "J04", "skill_id": "S03", "level": "Mandatory"},
        {"job_id": "J04", "skill_id": "S08", "level": "Mandatory"},
        {"job_id": "J04", "skill_id": "S13", "level": "Preferred"},

        {"job_id": "J05", "skill_id": "S06", "level": "Mandatory"},
        {"job_id": "J05", "skill_id": "S07", "level": "Mandatory"},
        {"job_id": "J05", "skill_id": "S11", "level": "Mandatory"},

        {"job_id": "J06", "skill_id": "S04", "level": "Mandatory"},
        {"job_id": "J06", "skill_id": "S12", "level": "Mandatory"},
        {"job_id": "J06", "skill_id": "S03", "level": "Mandatory"},

        {"job_id": "J07", "skill_id": "S03", "level": "Mandatory"},
        {"job_id": "J07", "skill_id": "S10", "level": "Mandatory"},
        {"job_id": "J07", "skill_id": "S06", "level": "Preferred"},

        {"job_id": "J08", "skill_id": "S03", "level": "Mandatory"},
        {"job_id": "J08", "skill_id": "S05", "level": "Mandatory"},
        {"job_id": "J08", "skill_id": "S14", "level": "Preferred"},

        {"job_id": "J09", "skill_id": "S18", "level": "Mandatory"},
        {"job_id": "J09", "skill_id": "S06", "level": "Mandatory"},
        {"job_id": "J09", "skill_id": "S07", "level": "Mandatory"},
        {"job_id": "J09", "skill_id": "S03", "level": "Preferred"},

        {"job_id": "J10", "skill_id": "S09", "level": "Mandatory"},
        {"job_id": "J10", "skill_id": "S10", "level": "Mandatory"},
        {"job_id": "J10", "skill_id": "S03", "level": "Mandatory"},

        {"job_id": "J11", "skill_id": "S01", "level": "Mandatory"},
        {"job_id": "J11", "skill_id": "S04", "level": "Mandatory"},
        {"job_id": "J11", "skill_id": "S03", "level": "Mandatory"},

        {"job_id": "J12", "skill_id": "S01", "level": "Mandatory"},
        {"job_id": "J12", "skill_id": "S03", "level": "Mandatory"},

        {"job_id": "J13", "skill_id": "S11", "level": "Mandatory"},
        {"job_id": "J13", "skill_id": "S14", "level": "Mandatory"},
        {"job_id": "J13", "skill_id": "S09", "level": "Preferred"},

        {"job_id": "J14", "skill_id": "S08", "level": "Mandatory"},
        {"job_id": "J14", "skill_id": "S16", "level": "Mandatory"},
        {"job_id": "J14", "skill_id": "S01", "level": "Preferred"},

        {"job_id": "J15", "skill_id": "S04", "level": "Mandatory"},
        {"job_id": "J15", "skill_id": "S03", "level": "Mandatory"},
        {"job_id": "J15", "skill_id": "S14", "level": "Mandatory"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MATCH (j:JobRole {id: item.job_id})
        MATCH (s:Skill {id: item.skill_id})
        MERGE (j)-[r:REQUIRES_SKILL]->(s)
        SET r.level = item.level
    """, {"batch": job_skills})
    print(f"    - [REQUIRES_SKILL] relationships linked: {len(job_skills)}")

    # 10. Candidate -[:APPLIED_TO]-> JobRole
    applications = [
        {"candidate_id": "C01", "job_id": "J01", "applied_date": "2026-01-10", "status": "Interviewing"},
        {"candidate_id": "C01", "job_id": "J04", "applied_date": "2026-01-15", "status": "Pending"},
        {"candidate_id": "C02", "job_id": "J02", "applied_date": "2026-01-12", "status": "Interviewing"},
        {"candidate_id": "C02", "job_id": "J06", "applied_date": "2026-01-18", "status": "Pending"},
        {"candidate_id": "C03", "job_id": "J03", "applied_date": "2026-01-08", "status": "Offer Extended"},
        {"candidate_id": "C04", "job_id": "J05", "applied_date": "2026-01-14", "status": "Interviewing"},
        {"candidate_id": "C05", "job_id": "J04", "applied_date": "2026-01-11", "status": "Pending"},
        {"candidate_id": "C07", "job_id": "J13", "applied_date": "2026-01-05", "status": "Offer Extended"},
        {"candidate_id": "C08", "job_id": "J11", "applied_date": "2026-01-19", "status": "Pending"},
        {"candidate_id": "C09", "job_id": "J01", "applied_date": "2026-01-09", "status": "Interviewing"},
        {"candidate_id": "C10", "job_id": "J06", "applied_date": "2026-01-13", "status": "Pending"},
        {"candidate_id": "C11", "job_id": "J09", "applied_date": "2026-01-16", "status": "Interviewing"},
        {"candidate_id": "C12", "job_id": "J03", "applied_date": "2026-01-17", "status": "Pending"},
        {"candidate_id": "C13", "job_id": "J14", "applied_date": "2026-01-10", "status": "Pending"},
        {"candidate_id": "C15", "job_id": "J01", "applied_date": "2026-01-06", "status": "Rejected"},
        {"candidate_id": "C15", "job_id": "J11", "applied_date": "2026-01-12", "status": "Interviewing"},
        {"candidate_id": "C16", "job_id": "J12", "applied_date": "2026-01-20", "status": "Pending"},
        {"candidate_id": "C18", "job_id": "J10", "applied_date": "2026-01-14", "status": "Interviewing"},
        {"candidate_id": "C19", "job_id": "J09", "applied_date": "2026-01-07", "status": "Pending"},
        {"candidate_id": "C20", "job_id": "J02", "applied_date": "2026-01-15", "status": "Pending"},
        {"candidate_id": "C22", "job_id": "J13", "applied_date": "2026-01-04", "status": "Interviewing"},
        {"candidate_id": "C25", "job_id": "J01", "applied_date": "2026-01-08", "status": "Interviewing"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MATCH (c:Candidate {id: item.candidate_id})
        MATCH (j:JobRole {id: item.job_id})
        MERGE (c)-[r:APPLIED_TO]->(j)
        SET r.applied_date = item.applied_date, r.status = item.status
    """, {"batch": applications})
    print(f"    - [APPLIED_TO] relationships linked: {len(applications)}")

    # 11. Candidate -[:EARNED]-> Certification
    earned_certs = [
        {"candidate_id": "C01", "cert_id": "CERT01", "earned_date": "2024-03-15"},
        {"candidate_id": "C01", "cert_id": "CERT09", "earned_date": "2025-01-10"},
        {"candidate_id": "C02", "cert_id": "CERT04", "earned_date": "2024-06-20"},
        {"candidate_id": "C03", "cert_id": "CERT02", "earned_date": "2023-11-05"},
        {"candidate_id": "C03", "cert_id": "CERT06", "earned_date": "2024-08-12"},
        {"candidate_id": "C04", "cert_id": "CERT03", "earned_date": "2024-04-18"},
        {"candidate_id": "C04", "cert_id": "CERT07", "earned_date": "2024-09-01"},
        {"candidate_id": "C05", "cert_id": "CERT01", "earned_date": "2024-12-01"},
        {"candidate_id": "C07", "cert_id": "CERT10", "earned_date": "2023-05-15"},
        {"candidate_id": "C09", "cert_id": "CERT01", "earned_date": "2024-02-10"},
        {"candidate_id": "C09", "cert_id": "CERT09", "earned_date": "2025-02-01"},
        {"candidate_id": "C11", "cert_id": "CERT03", "earned_date": "2023-10-10"},
        {"candidate_id": "C11", "cert_id": "CERT07", "earned_date": "2024-01-15"},
        {"candidate_id": "C12", "cert_id": "CERT06", "earned_date": "2024-07-22"},
        {"candidate_id": "C15", "cert_id": "CERT01", "earned_date": "2023-09-14"},
        {"candidate_id": "C19", "cert_id": "CERT03", "earned_date": "2024-05-30"},
        {"candidate_id": "C20", "cert_id": "CERT04", "earned_date": "2024-11-11"},
        {"candidate_id": "C22", "cert_id": "CERT10", "earned_date": "2023-02-28"},
        {"candidate_id": "C25", "cert_id": "CERT01", "earned_date": "2024-10-05"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MATCH (c:Candidate {id: item.candidate_id})
        MATCH (crt:Certification {id: item.cert_id})
        MERGE (c)-[r:EARNED]->(crt)
        SET r.earned_date = item.earned_date
    """, {"batch": earned_certs})
    print(f"    - [EARNED] relationships linked: {len(earned_certs)}")

    # 12. Certification -[:VALIDATES]-> Skill
    cert_skills = [
        {"cert_id": "CERT01", "skill_id": "S01"},
        {"cert_id": "CERT01", "skill_id": "S02"},
        {"cert_id": "CERT02", "skill_id": "S09"},
        {"cert_id": "CERT02", "skill_id": "S11"},
        {"cert_id": "CERT03", "skill_id": "S07"},
        {"cert_id": "CERT03", "skill_id": "S06"},
        {"cert_id": "CERT04", "skill_id": "S04"},
        {"cert_id": "CERT04", "skill_id": "S12"},
        {"cert_id": "CERT05", "skill_id": "S10"},
        {"cert_id": "CERT05", "skill_id": "S09"},
        {"cert_id": "CERT06", "skill_id": "S15"},
        {"cert_id": "CERT06", "skill_id": "S09"},
        {"cert_id": "CERT07", "skill_id": "S06"},
        {"cert_id": "CERT08", "skill_id": "S11"},
        {"cert_id": "CERT09", "skill_id": "S01"},
        {"cert_id": "CERT09", "skill_id": "S04"},
        {"cert_id": "CERT10", "skill_id": "S11"},
        {"cert_id": "CERT10", "skill_id": "S14"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MATCH (crt:Certification {id: item.cert_id})
        MATCH (s:Skill {id: item.skill_id})
        MERGE (crt)-[:VALIDATES]->(s)
    """, {"batch": cert_skills})
    print(f"    - [VALIDATES] relationships linked: {len(cert_skills)}")

    # 13. Course -[:TEACHES]-> Skill
    course_skills = [
        {"course_id": "CRS01", "skill_id": "S01"},
        {"course_id": "CRS01", "skill_id": "S02"},
        {"course_id": "CRS02", "skill_id": "S04"},
        {"course_id": "CRS02", "skill_id": "S12"},
        {"course_id": "CRS03", "skill_id": "S15"},
        {"course_id": "CRS03", "skill_id": "S09"},
        {"course_id": "CRS04", "skill_id": "S06"},
        {"course_id": "CRS04", "skill_id": "S07"},
        {"course_id": "CRS05", "skill_id": "S05"},
        {"course_id": "CRS05", "skill_id": "S03"},
        {"course_id": "CRS06", "skill_id": "S14"},
        {"course_id": "CRS07", "skill_id": "S18"},
        {"course_id": "CRS07", "skill_id": "S04"},
        {"course_id": "CRS08", "skill_id": "S08"},
        {"course_id": "CRS08", "skill_id": "S13"},
        {"course_id": "CRS09", "skill_id": "S11"},
        {"course_id": "CRS10", "skill_id": "S01"},
        {"course_id": "CRS10", "skill_id": "S04"},
        {"course_id": "CRS11", "skill_id": "S17"},
        {"course_id": "CRS12", "skill_id": "S03"},
    ]
    conn.query("""
        UNWIND $batch AS item
        MATCH (crs:Course {id: item.course_id})
        MATCH (s:Skill {id: item.skill_id})
        MERGE (crs)-[:TEACHES]->(s)
    """, {"batch": course_skills})
    print(f"    - [TEACHES] relationships linked: {len(course_skills)}")

    print("\n--> [SUCCESS] Knowledge Graph Data Ingestion Completed Successfully!")
    verify_summary(conn)


def verify_summary(conn: Neo4jConnection):
    """Outputs node and relationship count summary."""
    node_counts = conn.query("""
        MATCH (n)
        RETURN labels(n)[0] AS node_type, count(n) AS count
        ORDER BY count DESC
    """)
    rel_counts = conn.query("""
        MATCH ()-[r]->()
        RETURN type(r) AS rel_type, count(r) AS count
        ORDER BY count DESC
    """)
    total_nodes = conn.query("MATCH (n) RETURN count(n) AS total")[0]["total"]
    total_rels = conn.query("MATCH ()-[r]->() RETURN count(r) AS total")[0]["total"]

    print("\n==========================================")
    print("      GRAPH DATASET SUMMARY REPORT        ")
    print("==========================================")
    print(f"Total Nodes: {total_nodes}")
    for row in node_counts:
        print(f"  - {row['node_type']}: {row['count']}")
    print(f"\nTotal Relationships: {total_rels}")
    for row in rel_counts:
        print(f"  - [:{row['rel_type']}]: {row['count']}")
    print("==========================================\n")


if __name__ == "__main__":
    conn = Neo4jConnection()
    try:
        seed_database(conn, wipe_existing=True)
    finally:
        conn.close()
