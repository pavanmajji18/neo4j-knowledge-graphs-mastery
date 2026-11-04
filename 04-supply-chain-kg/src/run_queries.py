import sys
from connection import get_driver

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

QUERIES = {
    "1. Products depending on Supplier A (Alpha Chipsets)": """
        MATCH (s:Supplier {id: 'S_A'})-[:SUPPLIES]->(c:Component)-[:USED_IN]->(p:Product)
        RETURN s.name AS Supplier, c.name AS Component, p.name AS Product, p.sku AS SKU
    """,
    "2. Plants affected if Component X (C_X) becomes unavailable": """
        MATCH (c:Component {id: 'C_X'})-[:USED_IN]->(p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
        RETURN c.name AS DisruptedComponent, p.name AS Product, pl.name AS ImpactedPlant, pl.city AS PlantLocation
    """,
    "3. All suppliers connected to Product Y (Smart Watch Pro)": """
        MATCH (p:Product {id: 'P_Y'})<-[:USED_IN]-(c:Component)<-[:SUPPLIES]-(s:Supplier)
        OPTIONAL MATCH (s)<-[:SUPPLIES_TO]-(t2:Supplier)
        RETURN p.name AS Product, c.name AS Component, s.name AS DirectSupplier, t2.name AS Tier2Supplier
    """,
    "4. Dependency path between Tier-2 Supplier and Plant": """
        MATCH path = (t2:Supplier {tier: 2})-[:SUPPLIES_TO]->(t1:Supplier)-[:SUPPLIES]->(c:Component)-[:USED_IN]->(p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
        RETURN [node in nodes(path) | coalesce(node.name, labels(node)[0])] AS TraversalPath, length(path) AS Hops
    """,
    "5. Components supplied from Germany (DE) used in products": """
        MATCH (cou:Country {id: 'DE'})<-[:LOCATED_IN]-(s:Supplier)-[:SUPPLIES]->(c:Component)-[:USED_IN]->(p:Product)
        RETURN cou.name AS OriginCountry, s.name AS Supplier, c.name AS Component, p.name AS Product
    """,
}


def execute_queries() -> None:
    with get_driver() as driver:
        with driver.session() as session:
            for title, query in QUERIES.items():
                print("\n==================================================")
                print(f"Executing: {title}")
                print("==================================================")
                records = [dict(record) for record in session.run(query)]
                if not records:
                    print("No results found.")
                for row in records:
                    print(row)


if __name__ == "__main__":
    execute_queries()
