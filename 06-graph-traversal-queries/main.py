from tabulate import tabulate
from connection import Neo4jConnection
from seed_graph import seed_database
from traversal_queries import GraphTraversalQueries

def print_result(title: str, records: list):
    print(f"\n=======================================================")
    print(f" {title}")
    print(f"=======================================================")
    if not records:
        print("No records found.")
        return
    headers = records[0].keys()
    rows = [[row[h] for h in headers] for row in records]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def main():
    # 1. Verify connection and seed data
    conn = Neo4jConnection()
    conn.verify_connection()
    seed_database()

    traverser = GraphTraversalQueries(conn.driver)

    try:
        # Q1
        print_result("Q1: Single-Hop Outgoing (Apex Semiconductors)",
                     traverser.q1_single_hop_outgoing("Apex Semiconductors"))

        # Q2
        print_result("Q2: Single-Hop Incoming (Components of Drone Pro)",
                     traverser.q2_single_hop_incoming("PRD-X1"))

        # Q3
        print_result("Q3: Two-Hop (Taiwan Suppliers to Downstream Products)",
                     traverser.q3_two_hop_supplier_to_product("Taiwan"))

        # Q4
        print_result("Q4: Multi-Hop 4-Node Chain (Supplier -> Component -> Product -> Plant)",
                     traverser.q4_full_supply_chain())

        # Q5
        print_result("Q5: Filtered Multi-Hop (Lead Time >= 30 days & USA Active Line)",
                     traverser.q5_filtered_path_by_lead_time_and_country(30, "USA"))

        # Q6
        print_result("Q6: Direction Analysis (Components sharing products with AI Tensor Processor)",
                     traverser.q6_undirected_co_component_usage("AI Tensor Processor"))

        # Q7
        print_result("Q7: Aggregation / Blast Radius Across Multi-Hop Chain",
                     traverser.q7_supplier_impact_aggregation())

        # Q8
        print_result("Q8: Variable-Length Traversal (*1..3 Recursive Dependencies)",
                     traverser.q8_variable_length_bom())

        # Q9
        print_result("Q9: Shortest Path (RawLithium Ltd SUP-04 to Austin Plant PLT-TX)",
                     traverser.q9_shortest_path("SUP-04", "PLT-TX"))

        # Q10
        print_result("Q10: Path Object Inspection (Node labels and Edge Types for PRD-M2)",
                     traverser.q10_path_object_inspection("PRD-M2"))

    finally:
        conn.close()
        print("\nAll queries executed. Connection closed.")

if __name__ == "__main__":
    main()