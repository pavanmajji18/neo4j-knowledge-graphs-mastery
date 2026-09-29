# 📦 04. Multi-Echelon Supply Chain Risk Knowledge Graph

[![Graph Database](https://img.shields.io/badge/Neo4j-AuraDB%20%2F%20Enterprise-008CC1.svg)](https://neo4j.com/)
[![Industry](https://img.shields.io/badge/Industry-Supply%20Chain%20%26%20Logistics-darkgreen.svg)]()
[![Analysis](https://img.shields.io/badge/Risk%20Analysis-Multi--Tier%20Traceability-blueviolet.svg)]()

This project builds a multi-echelon manufacturing supply chain Knowledge Graph in **Neo4j** using **Python**. It tracks multi-tier vendor dependencies, raw materials, component parts, product bills-of-materials (BOM), manufacturing assembly plants, logistics shipments, and country locations to enable sub-second disruption impact analysis.

---

## 🎯 Business Context & Problem Statement

Modern global manufacturing ecosystems suffer from hidden Tier-2 vendor dependencies. When a geopolitical crisis, natural disaster, or raw material shortage hits a Tier-2 vendor (e.g., silicon mining in Japan or wafer fabrication in Taiwan), supply chain managers traditionally struggle to identify which downstream assembly plants will stall.

### How this Knowledge Graph Solves It:
- **Tier-2 Visibility**: Traces hidden dependencies `(:Supplier Tier-2)-[:SUPPLIES_TO]->(:Supplier Tier-1)`.
- **Bill of Materials (BOM)**: Maps components into products `(:Component)-[:USED_IN]->(:Product)`.
- **Assembly Plant Impact**: Connects products to physical manufacturing plants `(:Product)-[:MANUFACTURED_AT]->(:Plant)`.
- **Logistics Tracking**: Associates in-transit shipments with components and destination assembly plants.

---

## 📐 Data Model & Graph Schema Specification

```mermaid
graph LR
    S2["(:Supplier Tier-2)"] -->|:SUPPLIES_TO {leadTimeDays}| S1["(:Supplier Tier-1)"]
    S1 -->|:SUPPLIES {unitCost}| C["(:Component)"]
    S2 -->|:SUPPLIES| C_Raw["(:Component)"]
    C -->|:USED_IN {quantity}| P["(:Product)"]
    P -->|:MANUFACTURED_AT| Plant["(:Plant)"]
    S1 -->|:LOCATED_IN| Ctr["(:Country)"]
    S2 -->|:LOCATED_IN| Ctr
    Shp["(:Shipment)"] -->|:CONTAINS {quantity}| C
    Shp -->|:DESTINED_FOR| Plant
```

### Entities & Node Properties

| Node Label | Count | Primary Attributes | Business Meaning |
|---|---|---|---|
| `Supplier` | 4 | `id`, `name`, `tier` | Tier-1 vendors (`Alpha Chipsets`) & Tier-2 vendors (`Silico Mining Co`). |
| `Component` | 4 | `id`, `name`, `category` | Raw materials (`Silicon Wafer`) and parts (`Processor MCU-101`, `OLED Display`). |
| `Product` | 2 | `id`, `name`, `sku` | Assembled end-user products (`Smart Watch Pro`, `Industrial Tablet`). |
| `Plant` | 2 | `id`, `name`, `city` | Assembly plants (`Austin Assembly Center`, `Dresden Tech Plant`). |
| `Shipment` | 2 | `id`, `trackingNo`, `status` | Active logistics shipments (`SH_001`, `SH_002`). |
| `Country` | 4 | `id`, `name` | Geographic locations (`Taiwan`, `Germany`, `United States`, `Japan`). |

### Relationship Properties

- `(:Supplier)-[:SUPPLIES_TO {leadTimeDays: 14}]->(:Supplier)`
- `(:Supplier)-[:SUPPLIES {unitCost: 18.50}]->(:Component)`
- `(:Component)-[:USED_IN {quantity: 1}]->(:Product)`
- `(:Shipment)-[:CONTAINS {quantity: 5000}]->(:Component)`

---

## 📁 Key Files & Architecture

- [`src/connection.py`](src/connection.py): Singleton Neo4j driver connection module using `.env` credentials.
- [`src/build_graph.py`](src/build_graph.py): Automated database wiping (`DETACH DELETE`) and graph seeding script.
- [`src/run_queries.py`](src/run_queries.py): Executable script running 5 business-critical risk analysis queries.
- [`requirements.txt`](requirements.txt): Module Python dependencies (`neo4j`, `python-dotenv`).

---

## 🔍 Featured Risk Analysis Cypher Queries

### Query 1: Tier-2 Supplier to Plant Multi-Hop Path
*Traces the complete 5-hop dependency path from a Tier-2 raw material supplier down to the assembly plant:*

```cypher
MATCH path = (t2:Supplier {tier: 2})-[:SUPPLIES_TO]->(t1:Supplier)-[:SUPPLIES]->(c:Component)-[:USED_IN]->(p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
RETURN [node in nodes(path) | coalesce(node.name, labels(node)[0])] AS TraversalPath, 
       length(path) AS Hops
```

### Query 2: Disruption Blast Radius Analysis
*Identifies which manufacturing plants stall if Component X (`Processor MCU-101`) is disrupted:*

```cypher
MATCH (c:Component {id: 'C_MCU101'})-[:USED_IN]->(p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
RETURN c.name AS DisruptedComponent, 
       p.name AS Product, 
       pl.name AS ImpactedPlant, 
       pl.city AS PlantLocation
```

---

## ⚡ Execution Instructions

```bash
# 1. Navigate to directory
cd 04-supply-chain-kg

# 2. Activate virtual environment & install requirements
python -m venv venv
.\venv\Scripts\activate  # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# 3. Create database schema & seed graph
python src/build_graph.py

# 4. Run risk analysis queries
python src/run_queries.py
```

---

## 🎤 How to Explain This Project to Technical Reviewers

- **For Technical Screeners**: *"In this project, I modeled a multi-echelon supply chain in Neo4j to solve the cascade disruption problem. By indexing 5-hop relationships between Tier-2 suppliers, Tier-1 vendors, components, products, and assembly plants, we can execute sub-millisecond impact analyses during regional supplier outages."*
- **For Non-Technical Managers**: *"If a factory in Taiwan shuts down, this Knowledge Graph instantly tells us which assembly plants in Texas will run out of parts, which products are affected, and what shipments are currently in transit."*