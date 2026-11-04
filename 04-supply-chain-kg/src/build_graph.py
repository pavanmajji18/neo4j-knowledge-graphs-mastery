import sys
from connection import get_driver

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CONSTRAINTS_CYPHER = [
    "CREATE CONSTRAINT country_id_unique IF NOT EXISTS FOR (c:Country) REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS FOR (s:Supplier) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT component_id_unique IF NOT EXISTS FOR (comp:Component) REQUIRE comp.id IS UNIQUE",
    "CREATE CONSTRAINT product_id_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE",
    "CREATE CONSTRAINT plant_id_unique IF NOT EXISTS FOR (pl:Plant) REQUIRE pl.id IS UNIQUE",
    "CREATE CONSTRAINT shipment_id_unique IF NOT EXISTS FOR (sh:Shipment) REQUIRE sh.id IS UNIQUE",
]

CLEAR_DB_CYPHER = "MATCH (n) DETACH DELETE n"

SEED_GRAPH_CYPHER = """
// 1. Merge Countries (4)
MERGE (c_tw:Country {id: 'TW'}) SET c_tw.name = 'Taiwan'
MERGE (c_de:Country {id: 'DE'}) SET c_de.name = 'Germany'
MERGE (c_us:Country {id: 'US'}) SET c_us.name = 'United States'
MERGE (c_jp:Country {id: 'JP'}) SET c_jp.name = 'Japan'

// 2. Merge Suppliers - Tier-2 and Tier-1 (4)
MERGE (s_tier2:Supplier {id: 'S_RAW'}) SET s_tier2.name = 'Silico Mining Co', s_tier2.tier = 2
MERGE (s_a:Supplier {id: 'S_A'}) SET s_a.name = 'Alpha Chipsets', s_a.tier = 1
MERGE (s_b:Supplier {id: 'S_B'}) SET s_b.name = 'Beta Displays', s_b.tier = 1
MERGE (s_c:Supplier {id: 'S_C'}) SET s_c.name = 'Gamma Sensors', s_c.tier = 1

// 3. Merge Components (4)
MERGE (comp_wafer:Component {id: 'C_WAFER'}) SET comp_wafer.name = 'Silicon Wafer', comp_wafer.category = 'Raw Material'
MERGE (comp_x:Component {id: 'C_X'}) SET comp_x.name = 'Processor MCU-101', comp_x.category = 'Microcontroller'
MERGE (comp_oled:Component {id: 'C_OLED'}) SET comp_oled.name = 'OLED Display 6-inch', comp_oled.category = 'Display'
MERGE (comp_gyro:Component {id: 'C_GYRO'}) SET comp_gyro.name = 'MEMS Gyroscope', comp_gyro.category = 'Sensor'

// 4. Merge Products (2)
MERGE (p_y:Product {id: 'P_Y'}) SET p_y.name = 'Smart Watch Pro', p_y.sku = 'SW-1000'
MERGE (p_tab:Product {id: 'P_TAB'}) SET p_tab.name = 'Industrial Tablet', p_tab.sku = 'IT-500'

// 5. Merge Plants (2)
MERGE (pl_austin:Plant {id: 'PL_ATX'}) SET pl_austin.name = 'Austin Assembly Center', pl_austin.city = 'Austin'
MERGE (pl_dresden:Plant {id: 'PL_DRS'}) SET pl_dresden.name = 'Dresden Tech Plant', pl_dresden.city = 'Dresden'

// 6. Merge Shipments (2)
MERGE (sh_1:Shipment {id: 'SH_001'}) SET sh_1.trackingNo = 'TRK-9871', sh_1.status = 'IN_TRANSIT'
MERGE (sh_2:Shipment {id: 'SH_002'}) SET sh_2.trackingNo = 'TRK-9872', sh_2.status = 'DELIVERED'

// 7. Merge Supplier Locations (4)
MERGE (s_tier2)-[:LOCATED_IN]->(c_jp)
MERGE (s_a)-[:LOCATED_IN]->(c_tw)
MERGE (s_b)-[:LOCATED_IN]->(c_de)
MERGE (s_c)-[:LOCATED_IN]->(c_us)

// 8. Merge Tier-2 to Tier-1 Dependencies & Tier-2 Supplies (2)
MERGE (s_tier2)-[r_t2_t1:SUPPLIES_TO]->(s_a) SET r_t2_t1.leadTimeDays = 14
MERGE (s_tier2)-[:SUPPLIES]->(comp_wafer)

// 9. Merge Tier-1 Supplies to Components (3)
MERGE (s_a)-[r_sa_cx:SUPPLIES]->(comp_x) SET r_sa_cx.unitCost = 18.5
MERGE (s_b)-[r_sb_oled:SUPPLIES]->(comp_oled) SET r_sb_oled.unitCost = 32.0
MERGE (s_c)-[r_sc_gyro:SUPPLIES]->(comp_gyro) SET r_sc_gyro.unitCost = 4.5

// 10. Merge Components Used in Products - BOM (4)
MERGE (comp_x)-[r_cx_py:USED_IN]->(p_y) SET r_cx_py.quantity = 1
MERGE (comp_oled)-[r_oled_py:USED_IN]->(p_y) SET r_oled_py.quantity = 1
MERGE (comp_gyro)-[r_gyro_py:USED_IN]->(p_y) SET r_gyro_py.quantity = 2
MERGE (comp_x)-[r_cx_ptab:USED_IN]->(p_tab) SET r_cx_ptab.quantity = 1

// 11. Merge Plants Manufacturing Products (2)
MERGE (p_y)-[:MANUFACTURED_AT]->(pl_austin)
MERGE (p_tab)-[:MANUFACTURED_AT]->(pl_dresden)

// 12. Merge Shipments (4)
MERGE (sh_1)-[r_sh1_cx:CONTAINS]->(comp_x) SET r_sh1_cx.quantity = 5000
MERGE (sh_1)-[:DESTINED_FOR]->(pl_austin)
MERGE (sh_2)-[r_sh2_oled:CONTAINS]->(comp_oled) SET r_sh2_oled.quantity = 2000
MERGE (sh_2)-[:DESTINED_FOR]->(pl_austin)
"""


def populate_database(reset: bool = True) -> None:
    with get_driver() as driver:
        with driver.session() as session:
            if reset:
                session.run(CLEAR_DB_CYPHER)
                print("🧹 Cleaned up existing database records.")

            for stmt in CONSTRAINTS_CYPHER:
                session.run(stmt)
            print("🔒 Enforced 6 uniqueness constraints across Supply Chain labels.")

            session.run(SEED_GRAPH_CYPHER)

            node_count = session.run("MATCH (n) RETURN count(n) AS count").single()["count"]
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) AS count").single()["count"]
            print(
                f"✅ Graph populated idempotently: {node_count} nodes and {rel_count} relationships."
            )


if __name__ == "__main__":
    populate_database(reset=True)
