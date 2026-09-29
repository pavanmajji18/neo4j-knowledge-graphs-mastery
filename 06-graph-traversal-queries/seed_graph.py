from connection import Neo4jConnection

SEED_QUERY = """
// 1. Clear previous sample data safely
MATCH (n) DETACH DELETE n;

// 2. Create Suppliers
CREATE (s1:Supplier {id: 'SUP-01', name: 'Apex Semiconductors', country: 'Taiwan', tier: 1})
CREATE (s2:Supplier {id: 'SUP-02', name: 'OpticWave Tech', country: 'South Korea', tier: 1})
CREATE (s3:Supplier {id: 'SUP-03', name: 'VoltBattery Co', country: 'Japan', tier: 2})
CREATE (s4:Supplier {id: 'SUP-04', name: 'RawLithium Ltd', country: 'Australia', tier: 3})

// 3. Create Components & Sub-components
CREATE (c1:Component {id: 'CMP-01', name: 'AI Tensor Processor', lead_time_days: 45, cost: 210.0})
CREATE (c2:Component {id: 'CMP-02', name: 'OLED Display Matrix', lead_time_days: 30, cost: 95.0})
CREATE (c3:Component {id: 'CMP-03', name: 'SolidState Battery Pack', lead_time_days: 60, cost: 130.0})
CREATE (c4:Component {id: 'CMP-04', name: 'Refined Cathode Core', lead_time_days: 20, cost: 45.0})

// 4. Create Products
CREATE (p1:Product {sku: 'PRD-X1', name: 'Autonomous Drone Pro', category: 'Robotics', retail_price: 1800.0})
CREATE (p2:Product {sku: 'PRD-M2', name: 'Edge AI Vision Hub', category: 'IoT', retail_price: 950.0})

// 5. Create Manufacturing Plants
CREATE (pl1:Plant {code: 'PLT-TX', name: 'Austin Assembly Facility', city: 'Austin', country: 'USA', capacity: 25000})
CREATE (pl2:Plant {code: 'PLT-DE', name: 'Stuttgart Automation Works', city: 'Stuttgart', country: 'Germany', capacity: 18000})

// 6. Connect Supplier -> Component
CREATE (s1)-[:SUPPLIES {unit_cost: 210.0, contract_year: 2024}]->(c1)
CREATE (s2)-[:SUPPLIES {unit_cost: 95.0, contract_year: 2025}]->(c2)
CREATE (s3)-[:SUPPLIES {unit_cost: 130.0, contract_year: 2024}]->(c3)
CREATE (s4)-[:SUPPLIES {unit_cost: 45.0, contract_year: 2023}]->(c4)

// 7. Connect Recursive Component Dependencies (BOM)
CREATE (c3)-[:DEPENDS_ON {qty: 2}]->(c4)

// 8. Connect Component -> Product
CREATE (c1)-[:PART_OF {quantity_required: 1}]->(p1)
CREATE (c2)-[:PART_OF {quantity_required: 1}]->(p1)
CREATE (c3)-[:PART_OF {quantity_required: 1}]->(p1)

CREATE (c1)-[:PART_OF {quantity_required: 2}]->(p2)
CREATE (c2)-[:PART_OF {quantity_required: 1}]->(p2)

// 9. Connect Product -> Plant
CREATE (p1)-[:MANUFACTURED_AT {line_id: 'L1', active: true}]->(pl1)
CREATE (p1)-[:MANUFACTURED_AT {line_id: 'L3', active: false}]->(pl2)
CREATE (p2)-[:MANUFACTURED_AT {line_id: 'L2', active: true}]->(pl2);
"""

def seed_database():
    conn = Neo4jConnection()
    with conn.driver.session() as session:
        for statement in SEED_QUERY.split(";"):
            stmt = statement.strip()
            if stmt:
                session.run(stmt)
        print("Supply chain graph seeded successfully.")
    conn.close()

if __name__ == "__main__":
    seed_database()