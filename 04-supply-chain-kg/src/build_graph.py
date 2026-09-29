from connection import get_driver

CLEAR_DB_CYPHER = """
MATCH (n) DETACH DELETE n
"""

CREATE_GRAPH_CYPHER = """
// 1. Create Countries
CREATE (c_tw:Country {id: 'TW', name: 'Taiwan'}),
       (c_de:Country {id: 'DE', name: 'Germany'}),
       (c_us:Country {id: 'US', name: 'United States'}),
       (c_jp:Country {id: 'JP', name: 'Japan'}),

// 2. Create Suppliers (Tier-1 and Tier-2)
       (s_tier2:Supplier {id: 'S_RAW', name: 'Silico Mining Co', tier: 2}),
       (s_a:Supplier {id: 'S_A', name: 'Alpha Chipsets', tier: 1}),
       (s_b:Supplier {id: 'S_B', name: 'Beta Displays', tier: 1}),
       (s_c:Supplier {id: 'S_C', name: 'Gamma Sensors', tier: 1}),

// 3. Create Components
       (comp_wafer:Component {id: 'C_WAFER', name: 'Silicon Wafer', category: 'Raw Material'}),
       (comp_x:Component {id: 'C_X', name: 'Processor MCU-101', category: 'Microcontroller'}),
       (comp_oled:Component {id: 'C_OLED', name: 'OLED Display 6-inch', category: 'Display'}),
       (comp_gyro:Component {id: 'C_GYRO', name: 'MEMS Gyroscope', category: 'Sensor'}),

// 4. Create Products
       (p_y:Product {id: 'P_Y', name: 'Smart Watch Pro', sku: 'SW-1000'}),
       (p_tab:Product {id: 'P_TAB', name: 'Industrial Tablet', sku: 'IT-500'}),

// 5. Create Plants
       (pl_austin:Plant {id: 'PL_ATX', name: 'Austin Assembly Center', city: 'Austin'}),
       (pl_dresden:Plant {id: 'PL_DRS', name: 'Dresden Tech Plant', city: 'Dresden'}),

// 6. Create Shipments
       (sh_1:Shipment {id: 'SH_001', trackingNo: 'TRK-9871', status: 'IN_TRANSIT'}),
       (sh_2:Shipment {id: 'SH_002', trackingNo: 'TRK-9872', status: 'DELIVERED'}),

// 7. Supplier Locations
       (s_tier2)-[:LOCATED_IN]->(c_jp),
       (s_a)-[:LOCATED_IN]->(c_tw),
       (s_b)-[:LOCATED_IN]->(c_de),
       (s_c)-[:LOCATED_IN]->(c_us),

// 8. Tier-2 to Tier-1 Dependencies & Tier-2 Supplies
       (s_tier2)-[:SUPPLIES_TO {leadTimeDays: 14}]->(s_a),
       (s_tier2)-[:SUPPLIES]->(comp_wafer),

// 9. Tier-1 Supplies to Components
       (s_a)-[:SUPPLIES {unitCost: 18.5}]->(comp_x),
       (s_b)-[:SUPPLIES {unitCost: 32.0}]->(comp_oled),
       (s_c)-[:SUPPLIES {unitCost: 4.5}]->(comp_gyro),

// 10. Components Used in Products (BOM)
       (comp_x)-[:USED_IN {quantity: 1}]->(p_y),
       (comp_oled)-[:USED_IN {quantity: 1}]->(p_y),
       (comp_gyro)-[:USED_IN {quantity: 2}]->(p_y),
       (comp_x)-[:USED_IN {quantity: 1}]->(p_tab),

// 11. Plants Manufacturing Products
       (p_y)-[:MANUFACTURED_AT]->(pl_austin),
       (p_tab)-[:MANUFACTURED_AT]->(pl_dresden),

// 12. Shipments
       (sh_1)-[:CONTAINS {quantity: 5000}]->(comp_x),
       (sh_1)-[:DESTINED_FOR]->(pl_austin),
       (sh_2)-[:CONTAINS {quantity: 2000}]->(comp_oled),
       (sh_2)-[:DESTINED_FOR]->(pl_austin)
"""

def populate_database():
    driver = get_driver()
    with driver.session() as session:
        # Step 1: Wipe existing nodes and relationships
        session.run(CLEAR_DB_CYPHER)
        print("🧹 Cleaned up existing database records.")

        # Step 2: Ingest the complete supply chain graph
        session.run(CREATE_GRAPH_CYPHER)
        print("✅ Graph successfully populated with Supply Chain data model.")
        
    driver.close()

if __name__ == "__main__":
    populate_database()