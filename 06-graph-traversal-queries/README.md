# 🧭 06. Advanced Graph Traversal & Multi-Hop Cypher Analytics

[![Cypher](https://img.shields.io/badge/Cypher-Multi--Hop%20Traversals-orange.svg)](https://neo4j.com/docs/cypher-manual/current/)
[![Algorithms](https://img.shields.io/badge/Graph%20Algorithms-shortestPath%20%7C%20Variable--Length-blueviolet.svg)]()
[![Tabular Output](https://img.shields.io/badge/Formatting-tabulate-blue.svg)]()

This project demonstrates **10 advanced graph traversal and analytical queries** in Cypher using Python and **Neo4j AuraDB**. It covers single-hop traversals, 4-hop chain traversals, path property filtering, direction analysis, fan-out aggregations, variable-length recursive traversals (`*1..3`), shortest path detection (`shortestPath()`), and path object inspection (`nodes(path)`, `relationships(path)`).

---

## 📐 Graph Topology & Data Model

```text
(:Supplier) -[:SUPPLIES]-> (:Component) -[:PART_OF]-> (:Product) -[:MANUFACTURED_AT]-> (:Plant)
                                |
                                +--[:DEPENDS_ON*1..3]-> (:Component)
```

- **Domain**: Global High-Tech Manufacturing Supply Chain.
- **Node Labels**: `Supplier`, `Component`, `Product`, `Plant`.
- **Relationship Types**: `:SUPPLIES`, `:PART_OF`, `:MANUFACTURED_AT`, `:DEPENDS_ON`.

---

## 📁 Architecture & Key Files

- [`connection.py`](connection.py): Neo4j driver connection manager.
- [`seed_graph.py`](seed_graph.py): Populates test dataset into Neo4j database using parameterized Cypher.
- [`traversal_queries.py`](traversal_queries.py): `GraphTraversalQueries` class encapsulating all 10 Cypher algorithms.
- [`main.py`](main.py): CLI runner executing queries and printing formatted `tabulate` grid results.
- [`requirements.txt`](requirements.txt): Module Python dependencies (`neo4j`, `python-dotenv`, `tabulate`).

---

## 🔍 Master Catalog of 10 Cypher Queries

| # | Query Pattern | Cypher Keyword / Concept | Description |
|---|---|---|---|
| **Q1** | Single-Hop Outgoing | `(s)-[:SUPPLIES]->(c)` | Finds all components supplied by a named supplier. |
| **Q2** | Single-Hop Incoming | `(p)<-[:PART_OF]-(c)` | Finds all components required for a specific product SKU. |
| **Q3** | Two-Hop Traversal | `(s)->(c)->(p)` | Maps suppliers in a target country to impacted end products. |
| **Q4** | 4-Node Chain | `(s)->(c)->(p)->(pl)` | Full end-to-end chain from supplier to manufacturing plant. |
| **Q5** | Path Property Filtering | `WHERE c.lead_time >= X AND pl.country = Y` | Filters paths based on component lead time & plant country. |
| **Q6** | Direction Analysis | `(c1)-[:PART_OF]->(p)<-[:PART_OF]-(c2)` | Finds co-occurring companion components sharing end products. |
| **Q7** | Fan-Out Aggregation | `count(DISTINCT p), count(DISTINCT pl)` | Computes downstream product & plant blast radius per supplier. |
| **Q8** | Variable-Length Recursive | `-[:DEPENDS_ON*1..3]->` | Traverses multi-level nested subcomponents in Bill-of-Materials. |
| **Q9** | Shortest Path | `shortestPath((s)-[*]-(pl))` | Discovers minimum hop distance between supplier & plant nodes. |
| **Q10** | Path Object Inspection | `nodes(path)`, `relationships(path)` | Extracts raw node labels and edge types along path instance. |

---

## 💻 Featured Cypher Code Snippets

### Q8: Variable-Length Recursive BOM Traversal (`*1..3`)
```cypher
MATCH (s:Supplier)-[:SUPPLIES]->(c1:Component)-[:DEPENDS_ON*1..3]->(c2:Component)
RETURN s.name AS primary_supplier, 
       c1.name AS parent_component, 
       c2.name AS nested_subcomponent
```

### Q9: Shortest Path Calculation
```cypher
MATCH (s:Supplier {id: $supplier_id}), (pl:Plant {code: $plant_code})
MATCH p = shortestPath((s)-[*]-(pl))
RETURN length(p) AS hops, 
       [n IN nodes(p) | coalesce(n.name, n.code)] AS path_nodes
```

### Q10: Path Object & Edge Type Extraction
```cypher
MATCH path = (s:Supplier)-[:SUPPLIES]->(c:Component)-[:PART_OF]->(p:Product {sku: $product_sku})
RETURN length(path) AS path_length,
       [n IN nodes(path) | labels(n)[0] + ':' + coalesce(n.name, n.sku)] AS node_labels,
       [r IN relationships(path) | type(r)] AS edge_types
```

---

## ⚡ Step-by-Step Setup & Execution

```bash
# 1. Navigate to directory
cd 06-graph-traversal-queries

# 2. Activate virtual environment & install dependencies
python -m venv venv
.\venv\Scripts\activate  # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# 3. Seed dataset & run all 10 traversal queries
python main.py
```

---

## 🎤 How to Explain This Project to Technical Reviewers

- **For Technical Screeners**: *"In this project, I implemented 10 multi-hop Cypher traversal patterns. I used variable-length path matching `*1..3` for recursive Bill-of-Materials, `shortestPath()` for graph distance calculation, and fan-out aggregations like `count(DISTINCT plant)` to measure vendor blast radius."*
- **For Non-Technical Managers**: *"This module showcases how Neo4j can instantly trace complex multi-step supply chains and calculate shortest routes between raw material vendors and factories."*