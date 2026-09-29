class GraphTraversalQueries:
    def __init__(self, driver):
        self.driver = driver

    # Query 1: Single-Hop Outgoing (Supplier -> Component)
    def q1_single_hop_outgoing(self, supplier_name: str):
        query = """
        MATCH (s:Supplier {name: $supplier_name})-[r:SUPPLIES]->(c:Component)
        RETURN s.name AS supplier, type(r) AS relationship, c.name AS component, c.cost AS cost
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query, supplier_name=supplier_name)]

    # Query 2: Single-Hop Incoming (Product <- Component)
    def q2_single_hop_incoming(self, product_sku: str):
        query = """
        MATCH (p:Product {sku: $product_sku})<-[r:PART_OF]-(c:Component)
        RETURN p.name AS product, c.name AS component, r.quantity_required AS qty
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query, product_sku=product_sku)]

    # Query 3: Two-Hop Traversal (Supplier -> Component -> Product)
    def q3_two_hop_supplier_to_product(self, supplier_country: str):
        query = """
        MATCH (s:Supplier {country: $supplier_country})-[:SUPPLIES]->(c:Component)-[:PART_OF]->(p:Product)
        RETURN s.name AS supplier, s.country AS country, c.name AS component, p.name AS impacted_product
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query, supplier_country=supplier_country)]

    # Query 4: Full Multi-Hop Chain (Supplier -> Component -> Product -> Plant)
    def q4_full_supply_chain(self):
        query = """
        MATCH (s:Supplier)-[:SUPPLIES]->(c:Component)-[:PART_OF]->(p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
        RETURN s.name AS supplier, c.name AS component, p.name AS product, pl.name AS plant, pl.country AS plant_country
        ORDER BY pl.name, p.name
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query)]

    # Query 5: Filtered Multi-Hop by Path Properties
    def q5_filtered_path_by_lead_time_and_country(self, min_lead_time: int, plant_country: str):
        query = """
        MATCH (s:Supplier)-[:SUPPLIES]->(c:Component)-[:PART_OF]->(p:Product)-[m:MANUFACTURED_AT]->(pl:Plant)
        WHERE c.lead_time_days >= $min_lead_time 
          AND pl.country = $plant_country 
          AND m.active = true
        RETURN s.name AS supplier, c.name AS component, c.lead_time_days AS lead_time, 
               p.name AS product, pl.name AS plant
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query, min_lead_time=min_lead_time, plant_country=plant_country)]

    # Query 6: Direction-Agnostic / Relationship Direction Analysis
    def q6_undirected_co_component_usage(self, component_name: str):
        query = """
        MATCH (c1:Component {name: $component_name})-[:PART_OF]->(p:Product)<-[:PART_OF]-(c2:Component)
        WHERE c1 <> c2
        RETURN p.name AS shared_product, collect(DISTINCT c2.name) AS companion_components
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query, component_name=component_name)]

    # Query 7: Aggregation and Fan-out Metrics Across Hops
    def q7_supplier_impact_aggregation(self):
        query = """
        MATCH (s:Supplier)-[:SUPPLIES]->(c:Component)-[:PART_OF]->(p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
        RETURN s.name AS supplier, 
               count(DISTINCT c) AS supplied_components, 
               count(DISTINCT p) AS supported_products, 
               count(DISTINCT pl) AS downstream_plants
        ORDER BY supported_products DESC
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query)]

    # Query 8: Variable-Length Traversal (Recursive BOM Dependencies)
    def q8_variable_length_bom(self):
        query = """
        MATCH (s:Supplier)-[:SUPPLIES]->(c1:Component)-[:DEPENDS_ON*1..3]->(c2:Component)
        RETURN s.name AS primary_supplier, c1.name AS parent_component, c2.name AS nested_subcomponent
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query)]

    # Query 9: Shortest Path Detection
    def q9_shortest_path(self, supplier_id: str, plant_code: str):
        query = """
        MATCH (s:Supplier {id: $supplier_id}), (pl:Plant {code: $plant_code})
        MATCH p = shortestPath((s)-[*]-(pl))
        RETURN length(p) AS hops, [n IN nodes(p) | coalesce(n.name, n.code)] AS path_nodes
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query, supplier_id=supplier_id, plant_code=plant_code)]

    # Query 10: Complete Path Object Extraction & Relationship Inspection
    def q10_path_object_inspection(self, product_sku: str):
        query = """
        MATCH path = (s:Supplier)-[:SUPPLIES]->(c:Component)-[:PART_OF]->(p:Product {sku: $product_sku})
        RETURN length(path) AS path_length,
               [n IN nodes(path) | labels(n)[0] + ':' + coalesce(n.name, n.sku)] AS node_labels,
               [r IN relationships(path) | type(r)] AS edge_types
        """
        with self.driver.session() as session:
            return [dict(rec) for rec in session.run(query, product_sku=product_sku)]