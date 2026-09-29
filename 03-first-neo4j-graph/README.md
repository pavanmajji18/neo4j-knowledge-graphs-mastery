# 🎓 03. EdTech Platform Knowledge Graph

[![Cypher](https://img.shields.io/badge/Cypher-DDL%20%2F%20DML-blue.svg)](https://neo4j.com/docs/cypher-manual/current/)
[![Graph Database](https://img.shields.io/badge/Neo4j-Aura%20%2F%20Desktop-008CC1.svg)](https://neo4j.com/)
[![Schema](https://img.shields.io/badge/Schema-22%20Nodes%20%7C%2027%20Edges-orange.svg)]()

This project builds an educational ecosystem Knowledge Graph modeling the relationships between **Students**, **Mentors**, **Courses**, **Skills**, **Projects**, and target hiring **Companies**. It showcases Cypher DDL/DML, property graph modeling, graph traversal, and CRUD execution in Neo4j.

---

## 🎯 Business Problem & Context

Educational technology platforms need to connect student learning paths directly with employer market demand. Traditional relational databases store this data across fragmented tables (`students`, `enrollments`, `courses`, `course_skills`, `skills`, `projects`), requiring 5-table `JOIN` queries to answer simple career questions.

Using Neo4j, this knowledge graph answers multi-entity questions instantly:
- *"Which students built projects requiring Cypher skills taught by Dr. Alicia Vance?"*
- *"What skills are missing for a student targeting hiring partner GraphTech Labs?"*

---

## 📐 Graph Topology & Data Model

```graph TD
    Student[":Student"] -->|ENROLLED_IN {enrolledOn}| Course[":Course"]
    Mentor[":Mentor"] -->|TEACHES| Course
    Course -->|TEACHES_SKILL| Skill[":Skill"]
    Student -->|BUILT| Project[":Project"]
    Project -->|USES| Skill
    Student -->|INTERESTED_IN {priority}| Company[":Company"]
```

### Node Metrics (22 Nodes Total)

| Node Label | Count | Primary Attributes | Description |
|---|---|---|---|
| `Student` | 6 | `id`, `name`, `level` | Learner profiles (`S01` - `S06`). |
| `Mentor` | 3 | `id`, `name`, `field` | Instructors (`M01` - `M03`). |
| `Course` | 3 | `code`, `title`, `credits` | Educational offerings (`CS101`, `CS102`, `CS103`). |
| `Skill` | 4 | `name`, `category` | Technical competencies (`Cypher`, `Python`, `Docker`, `GraphQL`). |
| `Project` | 3 | `id`, `name`, `difficulty` | Hands-on capstones (`P01` - `P03`). |
| `Company` | 3 | `id`, `name`, `location` | Hiring partners (`GraphTech Labs`, `NextGen Cloud`, `DataFlow Systems`). |

### Relationship Metrics (27 Relationships Total)

| Relationship Type | Source -> Target | Properties | Purpose |
|---|---|---|---|
| `:ENROLLED_IN` | `(:Student) -> (:Course)` | `enrolledOn` | Connects learners to enrolled courses. |
| `:TEACHES` | `(:Mentor) -> (:Course)` | N/A | Maps mentors to course offerings. |
| `:TEACHES_SKILL` | `(:Course) -> (:Skill)` | N/A | Maps course curricula to skills. |
| `:BUILT` | `(:Student) -> (:Project)` | N/A | Captures projects completed by students. |
| `:USES` | `(:Project) -> (:Skill)` | N/A | Defines technical stack required per project. |
| `:INTERESTED_IN` | `(:Student) -> (:Company)` | `priority` | Tracks candidate employment targets. |

---

## 📁 Key Files & Script Walkthrough

- [`cypher/01_seed_graph.cypher`](cypher/01_seed_graph.cypher): Idempotent Cypher script populating 22 nodes and 27 relationships using `MERGE`.
- [`cypher/02_crud_operations.cypher`](cypher/02_crud_operations.cypher): Cypher script demonstrating CREATE, MATCH, SET, and DETACH DELETE operations.
- [`src/connection.py`](src/connection.py): Neo4j driver connection manager using environment variables.
- [`src/build_graph.py`](src/build_graph.py): Python driver execution of graph seeding.
- [`src/crud_demo.py`](src/crud_demo.py): Python pipeline driving CRUD execution.

---

## 🔍 Featured Cypher Queries

### 1. Seeding Graph Idempotently with `MERGE`
```cypher
MERGE (s1:Student {id: "S01", name: "Aarav Sharma", level: "Beginner"})
MERGE (c1:Course {code: "CS101", title: "Neo4j & Knowledge Graphs", credits: 4})
MERGE (s1)-[:ENROLLED_IN {enrolledOn: "2026-01-10"}]->(c1)
```

### 2. Multi-Hop Pattern Matching
*Finds all students who built a project using the 'Cypher' skill:*
```cypher
MATCH (s:Student)-[:BUILT]->(p:Project)-[:USES]->(sk:Skill {name: "Cypher"})
RETURN s.name AS Student, p.name AS Project, sk.name AS Skill;
```

### 3. Safe Node & Relationship Deletion
```cypher
MATCH (s:Student {id: "S07"})
DETACH DELETE s;
```

---

## ⚡ Execution Instructions

### Option 1: Via Neo4j Browser / Bloom
1. Open Neo4j Browser connected to your AuraDB database.
2. Copy and paste the contents of [`cypher/01_seed_graph.cypher`](cypher/01_seed_graph.cypher) into the query bar and run.
3. Run queries from [`cypher/02_crud_operations.cypher`](cypher/02_crud_operations.cypher) to inspect results.

### Option 2: Via Python Driver
```bash
# 1. Navigate to directory
cd 03-first-neo4j-graph

# 2. Set up virtual environment
python -m venv venv
.\venv\Scripts\activate  # macOS/Linux: source venv/bin/activate

# 3. Install dependencies & run scripts
pip install -r requirements.txt
python src/build_graph.py
python src/crud_demo.py
```

---

## 🎤 How to Explain This Project to Technical Reviewers

- **For Technical Screeners**: *"In this project, I modeled a multi-entity EdTech domain using Cypher `MERGE` clauses to prevent duplicate nodes. I established 6 node types and 6 relationship types to model multi-hop queries like matching students to project tech stacks."*
- **For Non-Technical Managers**: *"This graph database connects students, courses, skills, and projects in one visual map, making it easy to identify which skills students acquire before applying to hiring companies."*
