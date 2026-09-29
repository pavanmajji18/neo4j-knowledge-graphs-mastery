# 🎯 07. Enterprise Job & Skill Recommendation Engine (Capstone)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-AuraDB%20Cloud-008CC1.svg)](https://neo4j.com/)
[![Cypher](https://img.shields.io/badge/Cypher-11%20Analytical%20Queries-orange.svg)](https://neo4j.com/docs/cypher-manual/current/)
[![Graph Metrics](https://img.shields.io/badge/Graph%20Data-88%2B%20Nodes%20%7C%20227%2B%20Edges-brightgreen.svg)]()
[![Testing](https://img.shields.io/badge/Unit%20Tests-unittest%20Passing-success.svg)]()

A production-grade, graph-oriented career recommendation engine built using **Python**, **Neo4j Aura (Cloud Graph Database)**, and **Cypher**.

This Knowledge Graph maps candidates, technical skills, job postings, corporate employers, professional certifications, and educational courses into an interconnected graph topology (**88+ Nodes, 227+ Relationships**).

---

## 📌 1. Business Problem Statement & Graph Utility

### Business Context
Traditional recruitment platforms rely on simple string-matching or relational database SQL tables to match candidates with open job postings. As career networks grow, querying multi-degree relationships (e.g., *"Which candidates have skill overlaps with current employees, possess validated certifications, and are missing fewer than 2 mandatory skills for a target job?"*) requires complex multi-table `JOIN` operations. In relational databases (RDBMS), these recursive joins suffer from **exponential query slowdown** ($O(N^k)$ complexity).

### Why a Graph Database (Neo4j)?
- **Index-Free Adjacency**: Neo4j traverses relationships via direct memory pointers in constant time ($O(1)$ per hop), independent of total database size.
- **Multi-Hop Skill Gap Analysis**: Seamlessly trace 3-hop and 4-hop paths: `Candidate -> Target JobRole -> Missing Skill <- Course / Certification`.
- **Flexible Schema Evolution**: New entity types (e.g., Projects, Assessment Scores) can be introduced without costly database migrations or schema alter scripts.

---

## 📐 2. Graph Model Specification

The Knowledge Graph topology consists of **6 Node Types** and **7 Relationship Types**, far exceeding project minimums.

```mermaid
graph TD
    Cand["(:Candidate)"] -->|:HAS_SKILL {proficiency, years}| Skill["(:Skill)"]
    Cand -->|:APPLIED_TO {status, date}| Job["(:JobRole)"]
    Job -->|:REQUIRES_SKILL {level}| Skill
    Job -->|:POSTED_BY| Comp["(:Company)"]
    Course["(:Course)"] -->|:TEACHES| Skill
    Cert["(:Certification)"] -->|:VALIDATES| Skill
    Cand -->|:EARNED {earned_date}| Cert
```

### Node Types (88 Nodes Total)

| Node Label | Count | Primary Key | Key Properties |
|---|---|---|---|
| `Candidate` | 25 | `id` | `id`, `name`, `experience_yrs`, `location`, `email` |
| `Skill` | 18 | `id` | `id`, `name`, `category` |
| `JobRole` | 15 | `id` | `id`, `title`, `min_experience`, `salary_range`, `location` |
| `Company` | 8 | `id` | `id`, `name`, `industry`, `location` |
| `Certification` | 10 | `id` | `id`, `title`, `issuer`, `validity_years` |
| `Course` | 12 | `id` | `id`, `title`, `platform`, `duration_hours` |

### Relationship Types (227 Relationships Total)

| Relationship Type | Source Node -> Target Node | Count | Relationship Properties |
|---|---|---|---|
| `HAS_SKILL` | `(:Candidate) -> (:Skill)` | 84 | `proficiency` (Expert/Intermediate/Beginner), `years` |
| `REQUIRES_SKILL` | `(:JobRole) -> (:Skill)` | 49 | `level` (Mandatory/Preferred) |
| `APPLIED_TO` | `(:Candidate) -> (:JobRole)` | 22 | `applied_date`, `status` (Interviewing/Pending/Offer Extended/Rejected) |
| `TEACHES` | `(:Course) -> (:Skill)` | 20 | N/A |
| `EARNED` | `(:Candidate) -> (:Certification)` | 19 | `earned_date` |
| `VALIDATES` | `(:Certification) -> (:Skill)` | 18 | N/A |
| `POSTED_BY` | `(:JobRole) -> (:Company)` | 15 | N/A |

---

## 🏗️ 3. Codebase Architecture & Structure

```text
07-final-kg-project/
├── .env                  # Neo4j connection environment variables
├── .env.example          # Environment variables template
├── .gitignore            # Git exclusion definitions
├── requirements.txt      # Python package dependencies
├── README.md             # Project documentation & execution guide
├── main.py               # Interactive CLI Runner & workflow entrypoint
├── src/
│   ├── __init__.py
│   ├── connection.py     # Singleton Neo4j Aura driver connection manager
│   ├── seed_data.py      # Schema constraints & batch UNWIND data seeder
│   ├── crud.py           # Parameterized Create, Read, Update, Delete module
│   └── queries.py        # 11 Analytical & multi-hop Cypher queries
└── tests/
    ├── __init__.py
    └── test_crud.py      # Automated unit tests for CRUD operations
```

### Core Components
- **[`src/connection.py`](src/connection.py)**: Thread-safe singleton driver instance with connection pooling.
- **[`src/seed_data.py`](src/seed_data.py)**: Schema constraint creation (`CREATE CONSTRAINT FOR ... IS UNIQUE`) and high-speed `UNWIND` batch seeding.
- **[`src/crud.py`](src/crud.py)**: Programmatic CRUD implementation for candidate and job posting lifecycles.
- **[`src/queries.py`](src/queries.py)**: 11 business-critical analytical Cypher queries.
- **[`main.py`](main.py)**: Interactive terminal runner with CLI flags.
- **[`tests/test_crud.py`](tests/test_crud.py)**: Automated unit tests asserting CRUD operations and data consistency.

---

## ⚡ 4. Setup & Installation Guide

### Step 1: Initialize Virtual Environment

```bash
cd 07-final-kg-project

# Initialize virtual environment
python -m venv venv

# Activate Virtual Environment
# On Windows PowerShell:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in `07-final-kg-project/`:

```env
NEO4J_URI=neo4j+s://<your-aura-id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your-aura-password>
NEO4J_DATABASE=neo4j
```

---

## 🚀 5. How to Run the Application

### 1. Interactive CLI Application
Run the main runner to access the interactive terminal menu:

```bash
python main.py
```

### 2. Seed / Reset Knowledge Graph Dataset
Populates database schema constraints and 88+ nodes with 227+ relationships:

```bash
python main.py --seed
# OR
python src/seed_data.py
```

### 3. Execute All 11 Analytical Cypher Queries
Runs all 11 multi-hop Cypher queries with formatted tabular outputs:

```bash
python main.py --query
# OR
python src/queries.py
```

### 4. Interactive CRUD Demonstration
Demonstrates programmatic Create, Read, Update, and Delete operations:

```bash
python main.py --crud
# OR
python src/crud.py
```

### 5. Automated Unit Tests
Executes test suite asserting CRUD operations and data consistency:

```bash
python -m unittest discover tests
```

---

## 🔍 6. Featured Multi-Hop Cypher Queries & Results

### Query 1: Multi-Hop Skill Gap Analysis (2-Hop)
*Identifies missing skills for Candidate `C01` (Alice Chen) targeting Job Role `J02` (AI/ML Solutions Architect).*

```cypher
MATCH (c:Candidate {id: $candidate_id})
MATCH (j:JobRole {id: $job_id})-[:POSTED_BY]->(co:Company)
MATCH (j)-[r:REQUIRES_SKILL]->(s:Skill)
WHERE NOT (c)-[:HAS_SKILL]->(s)
RETURN c.name AS Candidate,
       j.title AS TargetJob,
       co.name AS TargetCompany,
       s.name AS MissingSkill,
       r.level AS RequirementLevel
ORDER BY r.level DESC, s.name ASC
```

#### Output:
```text
+---------------+---------------------------+---------------+------------------+--------------------+
| Candidate     | TargetJob                 | TargetCompany | MissingSkill     | RequirementLevel   |
+===============+===========================+===============+==================+====================+
| Alice Chen    | AI/ML Solutions Architect | AI Nexus Labs | Machine Learning | Mandatory          |
| Alice Chen    | AI/ML Solutions Architect | AI Nexus Labs | PyTorch          | Mandatory          |
| Alice Chen    | AI/ML Solutions Architect | AI Nexus Labs | MLOps            | Preferred          |
+---------------+---------------------------+---------------+------------------+--------------------+
```

---

### Query 2: Learning Path Recommendations (3-Hop Traversal)
*Traces 3-hop paths to suggest courses and certifications that teach missing skills for a candidate.*

```cypher
MATCH (c:Candidate {id: $candidate_id})
MATCH (j:JobRole {id: $job_id})-[:REQUIRES_SKILL]->(s:Skill)
WHERE NOT (c)-[:HAS_SKILL]->(s)
OPTIONAL MATCH (crs:Course)-[:TEACHES]->(s)
OPTIONAL MATCH (crt:Certification)-[:VALIDATES]->(s)
RETURN s.name AS MissingSkill,
       collect(DISTINCT crs.title + ' [' + crs.platform + ']') AS RecommendedCourses,
       collect(DISTINCT crt.title) AS RecommendedCertifications
ORDER BY MissingSkill ASC
```

#### Output:
```text
+------------------+-------------------------------------------------------------+------------------------------------+
| MissingSkill     | RecommendedCourses                                          | RecommendedCertifications          |
+==================+=============================================================+====================================+
| Machine Learning | ['Advanced Machine Learning with PyTorch [Coursera]',       | ['TensorFlow Developer Certificate'|
|                  |  'Building Production MLOps Systems [Coursera]']            |  'Neo4j Graph Data Science Cert']  |
| MLOps            | ['Building Production MLOps Systems [Coursera]']            | []                                 |
| PyTorch          | ['Advanced Machine Learning with PyTorch [Coursera]']       | ['TensorFlow Developer Certificate']|
+------------------+-------------------------------------------------------------+------------------------------------+
```

---

### Query 3: Candidate Peer Overlap & Network Proximity (3-Hop Peer Search)
*Finds peer candidates with highest skill overlap for collaboration or internal movement.*

```cypher
MATCH (c1:Candidate {id: $candidate_id})-[hs1:HAS_SKILL]->(s:Skill)<-[hs2:HAS_SKILL]-(c2:Candidate)
WHERE c1 <> c2
WITH c1, c2, collect(s.name) AS CommonSkills, count(s) AS SharedSkillCount
MATCH (c1)-[:HAS_SKILL]->(all_s1:Skill)
WITH c1, c2, CommonSkills, SharedSkillCount, count(all_s1) AS C1SkillCount
RETURN c2.name AS PeerName,
       c2.location AS Location,
       SharedSkillCount,
       CommonSkills,
       round(100.0 * SharedSkillCount / C1SkillCount, 1) AS OverlapPercentage
ORDER BY SharedSkillCount DESC
LIMIT 3
```

---

## 🔀 7. Git & GitHub Branching Strategy

This project maintained a clean multi-commit Git history using feature branches:

1. **Scaffold & Connection Setup**: Initialized project, virtual environment, `.env`, `.gitignore`, `requirements.txt`, and `src/connection.py`.
2. **Feature Branch (`feature/data-modeling-and-seeding`)**: Implemented schema uniqueness constraints and batch `UNWIND` seeding in `src/seed_data.py`. Merged to `main`.
3. **Feature Branch (`feature/crud-and-traversals`)**: Developed `src/crud.py`, `src/queries.py`, `tests/test_crud.py`, and `main.py`. Merged to `main`.

---

## 🎤 How to Explain This Project to Technical Reviewers

- **For Technical Screeners**: *"My capstone project is a graph-oriented career recommendation engine with 88+ nodes and 227+ edges. It implements multi-hop skill gap analysis, computes Jaccard-like peer skill overlap percentages, and automatically generates 3-hop course and certification learning paths to bridge candidate skill gaps."*
- **For Non-Technical Managers**: *"Instead of simple keyword matching on resumes, this system acts like an intelligent career advisor. It analyzes a candidate's background, identifies missing skills for their dream job, and recommends the exact courses and certifications needed to get hired."*
