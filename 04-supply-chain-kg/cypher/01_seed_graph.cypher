// ==============================================================================
// 01_seed_graph.cypher
// Multi-Echelon Supply Chain Risk Knowledge Graph: Schema & Seed Script
// Compatible with Neo4j 5.x, Neo4j Browser, and Neo4j Aura Console
// ==============================================================================

// --- Step 1: Uniqueness Constraints (Neo4j 5.x) ---
CREATE CONSTRAINT country_id_unique IF NOT EXISTS FOR (c:Country) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS FOR (s:Supplier) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT component_id_unique IF NOT EXISTS FOR (comp:Component) REQUIRE comp.id IS UNIQUE;
CREATE CONSTRAINT product_id_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT plant_id_unique IF NOT EXISTS FOR (pl:Plant) REQUIRE pl.id IS UNIQUE;
CREATE CONSTRAINT shipment_id_unique IF NOT EXISTS FOR (sh:Shipment) REQUIRE sh.id IS UNIQUE;

// --- Step 2: Seed Nodes Idempotently (18 Nodes) ---
// 1. Merge Countries (4)
MERGE (c_tw:Country {id: 'TW'}) SET c_tw.name = 'Taiwan';
MERGE (c_de:Country {id: 'DE'}) SET c_de.name = 'Germany';
MERGE (c_us:Country {id: 'US'}) SET c_us.name = 'United States';
MERGE (c_jp:Country {id: 'JP'}) SET c_jp.name = 'Japan';

// 2. Merge Suppliers - Tier-2 and Tier-1 (4)
MERGE (s_raw:Supplier {id: 'S_RAW'}) SET s_raw.name = 'Silico Mining Co', s_raw.tier = 2;
MERGE (s_a:Supplier {id: 'S_A'}) SET s_a.name = 'Alpha Chipsets', s_a.tier = 1;
MERGE (s_b:Supplier {id: 'S_B'}) SET s_b.name = 'Beta Displays', s_b.tier = 1;
MERGE (s_c:Supplier {id: 'S_C'}) SET s_c.name = 'Gamma Sensors', s_c.tier = 1;

// 3. Merge Components (4)
MERGE (comp_wafer:Component {id: 'C_WAFER'}) SET comp_wafer.name = 'Silicon Wafer', comp_wafer.category = 'Raw Material';
MERGE (comp_x:Component {id: 'C_X'}) SET comp_x.name = 'Processor MCU-101', comp_x.category = 'Microcontroller';
MERGE (comp_oled:Component {id: 'C_OLED'}) SET comp_oled.name = 'OLED Display 6-inch', comp_oled.category = 'Display';
MERGE (comp_gyro:Component {id: 'C_GYRO'}) SET comp_gyro.name = 'MEMS Gyroscope', comp_gyro.category = 'Sensor';

// 4. Merge Products (2)
MERGE (p_y:Product {id: 'P_Y'}) SET p_y.name = 'Smart Watch Pro', p_y.sku = 'SW-1000';
MERGE (p_tab:Product {id: 'P_TAB'}) SET p_tab.name = 'Industrial Tablet', p_tab.sku = 'IT-500';

// 5. Merge Plants (2)
MERGE (pl_austin:Plant {id: 'PL_ATX'}) SET pl_austin.name = 'Austin Assembly Center', pl_austin.city = 'Austin';
MERGE (pl_dresden:Plant {id: 'PL_DRS'}) SET pl_dresden.name = 'Dresden Tech Plant', pl_dresden.city = 'Dresden';

// 6. Merge Shipments (2)
MERGE (sh_1:Shipment {id: 'SH_001'}) SET sh_1.trackingNo = 'TRK-9871', sh_1.status = 'IN_TRANSIT';
MERGE (sh_2:Shipment {id: 'SH_002'}) SET sh_2.trackingNo = 'TRK-9872', sh_2.status = 'DELIVERED';

// --- Step 3: Seed Relationships Idempotently (19 Relationships) ---
// 7. Merge Supplier Locations (4 :LOCATED_IN)
MATCH (s:Supplier {id: 'S_RAW'}), (c:Country {id: 'JP'})
MERGE (s)-[:LOCATED_IN]->(c);

MATCH (s:Supplier {id: 'S_A'}), (c:Country {id: 'TW'})
MERGE (s)-[:LOCATED_IN]->(c);

MATCH (s:Supplier {id: 'S_B'}), (c:Country {id: 'DE'})
MERGE (s)-[:LOCATED_IN]->(c);

MATCH (s:Supplier {id: 'S_C'}), (c:Country {id: 'US'})
MERGE (s)-[:LOCATED_IN]->(c);

// 8. Merge Tier-2 Dependencies & Supplies (1 :SUPPLIES_TO, 1 :SUPPLIES)
MATCH (t2:Supplier {id: 'S_RAW'}), (t1:Supplier {id: 'S_A'})
MERGE (t2)-[r:SUPPLIES_TO]->(t1) SET r.leadTimeDays = 14;

MATCH (s:Supplier {id: 'S_RAW'}), (comp:Component {id: 'C_WAFER'})
MERGE (s)-[:SUPPLIES]->(comp);

// 9. Merge Tier-1 Supplies to Components (3 :SUPPLIES)
MATCH (s:Supplier {id: 'S_A'}), (comp:Component {id: 'C_X'})
MERGE (s)-[r:SUPPLIES]->(comp) SET r.unitCost = 18.5;

MATCH (s:Supplier {id: 'S_B'}), (comp:Component {id: 'C_OLED'})
MERGE (s)-[r:SUPPLIES]->(comp) SET r.unitCost = 32.0;

MATCH (s:Supplier {id: 'S_C'}), (comp:Component {id: 'C_GYRO'})
MERGE (s)-[r:SUPPLIES]->(comp) SET r.unitCost = 4.5;

// 10. Merge Components Used in Products - BOM (4 :USED_IN)
MATCH (comp:Component {id: 'C_X'}), (p:Product {id: 'P_Y'})
MERGE (comp)-[r:USED_IN]->(p) SET r.quantity = 1;

MATCH (comp:Component {id: 'C_OLED'}), (p:Product {id: 'P_Y'})
MERGE (comp)-[r:USED_IN]->(p) SET r.quantity = 1;

MATCH (comp:Component {id: 'C_GYRO'}), (p:Product {id: 'P_Y'})
MERGE (comp)-[r:USED_IN]->(p) SET r.quantity = 2;

MATCH (comp:Component {id: 'C_X'}), (p:Product {id: 'P_TAB'})
MERGE (comp)-[r:USED_IN]->(p) SET r.quantity = 1;

// 11. Merge Plants Manufacturing Products (2 :MANUFACTURED_AT)
MATCH (p:Product {id: 'P_Y'}), (pl:Plant {id: 'PL_ATX'})
MERGE (p)-[:MANUFACTURED_AT]->(pl);

MATCH (p:Product {id: 'P_TAB'}), (pl:Plant {id: 'PL_DRS'})
MERGE (p)-[:MANUFACTURED_AT]->(pl);

// 12. Merge Shipments (2 :CONTAINS, 2 :DESTINED_FOR)
MATCH (sh:Shipment {id: 'SH_001'}), (comp:Component {id: 'C_X'})
MERGE (sh)-[r:CONTAINS]->(comp) SET r.quantity = 5000;

MATCH (sh:Shipment {id: 'SH_001'}), (pl:Plant {id: 'PL_ATX'})
MERGE (sh)-[:DESTINED_FOR]->(pl);

MATCH (sh:Shipment {id: 'SH_002'}), (comp:Component {id: 'C_OLED'})
MERGE (sh)-[r:CONTAINS]->(comp) SET r.quantity = 2000;

MATCH (sh:Shipment {id: 'SH_002'}), (pl:Plant {id: 'PL_ATX'})
MERGE (sh)-[:DESTINED_FOR]->(pl);

