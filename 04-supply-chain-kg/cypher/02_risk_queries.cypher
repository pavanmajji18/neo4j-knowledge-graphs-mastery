// ==============================================================================
// 02_risk_queries.cypher
// Multi-Echelon Supply Chain Risk & Traceability Queries
// Compatible with Neo4j 5.x, Neo4j Browser, and Neo4j Aura Console
// ==============================================================================

// --- Query 1: Products depending on Supplier A (Alpha Chipsets) ---
MATCH (s:Supplier {id: 'S_A'})-[:SUPPLIES]->(c:Component)-[:USED_IN]->(p:Product)
RETURN s.name AS Supplier, c.name AS Component, p.name AS Product, p.sku AS SKU;

// --- Query 2: Plants affected if Component X (C_X) becomes unavailable ---
MATCH (c:Component {id: 'C_X'})-[:USED_IN]->(p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
RETURN c.name AS DisruptedComponent, p.name AS Product, pl.name AS ImpactedPlant, pl.city AS PlantLocation;

// --- Query 3: All suppliers connected to Product Y (Smart Watch Pro) ---
MATCH (p:Product {id: 'P_Y'})<-[:USED_IN]-(c:Component)<-[:SUPPLIES]-(s:Supplier)
OPTIONAL MATCH (s)<-[:SUPPLIES_TO]-(t2:Supplier)
RETURN p.name AS Product, c.name AS Component, s.name AS DirectSupplier, t2.name AS Tier2Supplier;

// --- Query 4: Dependency path between Tier-2 Supplier and Plant (5-node, 4-hop path) ---
MATCH path = (t2:Supplier {tier: 2})-[:SUPPLIES_TO]->(t1:Supplier)-[:SUPPLIES]->(c:Component)-[:USED_IN]->(p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
RETURN [node in nodes(path) | coalesce(node.name, labels(node)[0])] AS TraversalPath, length(path) AS Hops;

// --- Query 5: Components supplied from Germany (DE) used in products ---
MATCH (cou:Country {id: 'DE'})<-[:LOCATED_IN]-(s:Supplier)-[:SUPPLIES]->(c:Component)-[:USED_IN]->(p:Product)
RETURN cou.name AS OriginCountry, s.name AS Supplier, c.name AS Component, p.name AS Product;

// --- Query 6: In-transit shipment mitigation for Component X (C_X) ---
MATCH (sh:Shipment {status: 'IN_TRANSIT'})-[r:CONTAINS]->(c:Component {id: 'C_X'}),
      (sh)-[:DESTINED_FOR]->(pl:Plant)
RETURN sh.trackingNo AS TrackingNumber, sh.status AS ShipmentStatus, c.name AS Component, r.quantity AS InTransitQuantity, pl.name AS DestinationPlant, pl.city AS DestinationCity;
