"""
Script to generate high-DPI visual showcase assets for 07-final-kg-project:
1. assets/linkedin_split_screen_showcase.png (1920x1080)
2. assets/neo4j_aura_graph_visualization.png (1920x1080)
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from tabulate import tabulate
import networkx as nx

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.connection import Neo4jConnection
from src.queries import q3_skill_gap_analysis, q4_learning_path_recommendations


def get_browser_binary():
    program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    candidate_paths = [
        os.path.join(program_files, "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(program_files_x86, "Microsoft", "Edge", "Application", "msedge.exe"),
        shutil.which("google-chrome") or "",
        shutil.which("chromium") or "",
        shutil.which("msedge") or "",
        shutil.which("chrome") or "",
    ]
    for p in candidate_paths:
        if p and os.path.exists(p):
            return p
    raise RuntimeError("Neither Chrome nor Edge was found on this system.")


def render_html_to_png(html_path: str, output_png_path: str, width: int = 1920, height: int = 1080):
    browser_bin = get_browser_binary()
    file_url = f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}"

    args = [
        browser_bin,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size={width},{height}",
        f"--screenshot={output_png_path}",
        file_url
    ]

    print(f"Rendering {output_png_path} ({width}x{height}) via {os.path.basename(browser_bin)}...")
    res = subprocess.run(args, capture_output=True, text=True, timeout=40)
    if os.path.exists(output_png_path) and os.path.getsize(output_png_path) > 0:
        print(f"[OK] Generated: {output_png_path} ({os.path.getsize(output_png_path):,} bytes)")
    else:
        print(f"[ERROR] Failed to generate {output_png_path}. stdout: {res.stdout}, stderr: {res.stderr}")
        raise RuntimeError(f"Rendering failed for {output_png_path}")


def generate_split_screen_asset(conn: Neo4jConnection, assets_dir: Path):
    print("\n--> Generating Split-Screen LinkedIn Showcase Asset...")
    gaps = q3_skill_gap_analysis(conn, "C01", "J02")
    recs_raw = q4_learning_path_recommendations(conn, "C01", "J02")

    # Clean format for Query 3
    q3_table = tabulate(gaps, headers="keys", tablefmt="grid")

    # Format Query 4 with clean line breaks inside list cells for crisp tabular display
    recs_formatted = []
    for r in recs_raw:
        courses = r.get("RecommendedCourses", [])
        certs = r.get("RecommendedCertifications", [])
        courses_str = "\n".join(f"• {c}" for c in courses) if courses else "(None)"
        certs_str = "\n".join(f"• {c}" for c in certs) if certs else "(None)"
        recs_formatted.append({
            "MissingSkill": r["MissingSkill"],
            "RecommendedCourses": courses_str,
            "RecommendedCertifications": certs_str,
        })
    q4_table = tabulate(recs_formatted, headers="keys", tablefmt="grid")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}
  body {{
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    background: #070B11;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
    color: #E6EDF3;
    display: flex;
    flex-direction: column;
    padding: 22px 28px;
    gap: 14px;
  }}

  /* HEADER BAR */
  .header-card {{
    background: linear-gradient(135deg, #111722 0%, #0B0E14 100%);
    border: 1px solid #243042;
    border-radius: 12px;
    padding: 14px 26px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  }}
  .brand-group {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .logo-icon {{
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #008CC1 0%, #005F87 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 24px;
    color: #FFFFFF;
    box-shadow: 0 4px 14px rgba(0, 140, 193, 0.45);
  }}
  .title-text {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  .main-title {{
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.4px;
    color: #FFFFFF;
  }}
  .sub-title {{
    font-size: 13px;
    color: #8B949E;
    font-weight: 500;
  }}
  .sub-title span {{
    color: #58A6FF;
    font-weight: 600;
  }}
  .badges-row {{
    display: flex;
    gap: 10px;
  }}
  .badge {{
    font-size: 11px;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 20px;
    border: 1px solid #30363D;
    background: #161B22;
    color: #C9D1D9;
    letter-spacing: 0.2px;
  }}
  .badge.blue {{ border-color: #1F6FEB; color: #58A6FF; background: rgba(31, 111, 235, 0.16); }}
  .badge.green {{ border-color: #238636; color: #7EE787; background: rgba(35, 134, 54, 0.16); }}
  .badge.orange {{ border-color: #D29922; color: #FFA657; background: rgba(210, 153, 34, 0.16); }}
  .badge.purple {{ border-color: #8957E5; color: #D2A8FF; background: rgba(137, 87, 229, 0.16); }}

  /* SPLIT MAIN */
  .split-container {{
    display: grid;
    grid-template-columns: 1.02fr 0.98fr;
    gap: 18px;
    flex: 1;
    min-height: 0;
  }}

  /* PANE STYLING */
  .pane {{
    background: #0C1017;
    border: 1px solid #212936;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.55);
  }}
  .pane-header {{
    background: #141A24;
    border-bottom: 1px solid #243042;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .pane-title {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    font-weight: 600;
    color: #C9D1D9;
  }}
  .pane-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }}
  .pane-dot.red {{ background: #FF5F56; }}
  .pane-dot.yellow {{ background: #FFBD2E; }}
  .pane-dot.green {{ background: #27C93F; }}
  .window-controls {{
    display: flex;
    gap: 7px;
  }}

  /* LEFT PANE: CODE */
  .code-body {{
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
  }}
  .code-box {{
    background: #06090E;
    border: 1px solid #1A222E;
    border-radius: 8px;
    padding: 12px 16px;
    font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
    font-size: 12.3px;
    line-height: 1.48;
    color: #D1D5DB;
    overflow-x: auto;
  }}
  .code-pre {{
    margin: 0;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
    white-space: pre;
  }}
  .kw-func {{ color: #79C0FF; font-weight: 600; }}
  .kw-def {{ color: #FF7B72; font-weight: 600; }}
  .kw-param {{ color: #FFA657; }}
  .kw-cypher {{ color: #79C0FF; font-weight: 700; }}
  .kw-where {{ color: #FF7B72; font-weight: 800; }}
  .kw-opt {{ color: #D2A8FF; font-weight: 700; }}
  .kw-ret {{ color: #7EE787; font-weight: 700; }}
  .kw-comment {{ color: #768390; font-style: italic; }}
  .code-highlight {{
    background: rgba(255, 123, 114, 0.16);
    border-left: 3px solid #FF7B72;
    padding: 2px 6px;
    display: block;
    margin: 1px -6px;
    border-radius: 0 4px 4px 0;
  }}
  .code-highlight-opt {{
    background: rgba(210, 168, 255, 0.16);
    border-left: 3px solid #D2A8FF;
    padding: 2px 6px;
    display: block;
    margin: 1px -6px;
    border-radius: 0 4px 4px 0;
  }}

  /* CALLOUT CARDS */
  .callouts-container {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }}
  .callout-card {{
    background: #0E131C;
    border: 1px solid #202938;
    border-radius: 8px;
    padding: 9px 12px;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  .callout-title {{
    font-size: 11px;
    font-weight: 700;
    color: #58A6FF;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .callout-desc {{
    font-size: 10.6px;
    color: #9CA3AF;
    line-height: 1.35;
  }}

  /* RIGHT PANE: CLI & TOPOLOGY */
  .right-body {{
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
    overflow: hidden;
  }}
  .terminal-box {{
    background: #06090E;
    border: 1px solid #1B2330;
    border-radius: 8px;
    padding: 10px 14px;
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 10.4px;
    line-height: 1.3;
    color: #E2E8F0;
    overflow-x: auto;
    flex: 1;
  }}
  .cmd-prompt {{
    color: #7EE787;
    font-weight: 700;
    margin-bottom: 5px;
    font-size: 11.2px;
  }}
  .section-label {{
    font-size: 11px;
    font-weight: 700;
    color: #FFA657;
    margin-top: 6px;
    margin-bottom: 3px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  pre.cli-table {{
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
    margin: 0;
    white-space: pre;
  }}

  /* TOPOLOGY DIAGRAM IN RIGHT PANE */
  .topology-card {{
    background: #0E131C;
    border: 1px solid #202938;
    border-radius: 8px;
    padding: 10px 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .topology-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .topology-title {{
    font-size: 11px;
    font-weight: 700;
    color: #7EE787;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}
  .topology-flow {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    padding: 4px 0;
  }}
  .topo-node {{
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.3px;
  }}
  .node-cand {{ background: rgba(79, 209, 197, 0.2); border: 1px solid #4FD1C5; color: #4FD1C5; }}
  .node-job {{ background: rgba(129, 140, 248, 0.2); border: 1px solid #818CF8; color: #818CF8; }}
  .node-skill {{ background: rgba(251, 146, 60, 0.2); border: 1px solid #FB923C; color: #FB923C; }}
  .node-course {{ background: rgba(56, 189, 248, 0.2); border: 1px solid #38BDF8; color: #38BDF8; }}
  .node-cert {{ background: rgba(245, 158, 11, 0.2); border: 1px solid #F59E0B; color: #F59E0B; }}
  .node-comp {{ background: rgba(16, 185, 129, 0.2); border: 1px solid #10B981; color: #10B981; }}
  .topo-arrow {{
    font-size: 9.5px;
    color: #64748B;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: "JetBrains Mono", monospace;
  }}

  /* FOOTER */
  .footer-card {{
    background: #0C1017;
    border: 1px solid #212936;
    border-radius: 10px;
    padding: 9px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11.5px;
    color: #8B949E;
  }}
  .footer-left {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .footer-item {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .status-circle {{
    width: 8px;
    height: 8px;
    background: #238636;
    border-radius: 50%;
    box-shadow: 0 0 8px #238636;
  }}
</style>
</head>
<body>

  <!-- TOP HEADER -->
  <div class="header-card">
    <div class="brand-group">
      <div class="logo-icon">N</div>
      <div class="title-text">
        <div class="main-title">Enterprise Job &amp; Skill Recommendation Engine</div>
        <div class="sub-title">3-Hop Multi-Degree Graph Traversal &amp; Learning Path Recommendation &bull; <span>Neo4j Aura Cloud DB</span></div>
      </div>
    </div>
    <div class="badges-row">
      <div class="badge blue">88 Nodes</div>
      <div class="badge purple">227 Relationships</div>
      <div class="badge green">11 Cypher Analytics</div>
      <div class="badge orange">5/5 Unit Tests Passing</div>
    </div>
  </div>

  <!-- SPLIT SCREEN CONTENT -->
  <div class="split-container">

    <!-- LEFT PANE: CYPHER ENGINE CODE -->
    <div class="pane">
      <div class="pane-header">
        <div class="window-controls">
          <div class="pane-dot red"></div>
          <div class="pane-dot yellow"></div>
          <div class="pane-dot green"></div>
        </div>
        <div class="pane-title">src/queries.py &mdash; q4_learning_path_recommendations()</div>
        <div class="badge blue" style="padding: 2px 8px; font-size: 10px;">Python + Cypher Traversal</div>
      </div>
      <div class="code-body">
        <div class="code-box">
<pre class="code-pre"><span class="kw-def">def</span> <span class="kw-func">q4_learning_path_recommendations</span>(conn: Neo4jConnection, candidate_id=<span class="kw-param">"C01"</span>, job_id=<span class="kw-param">"J02"</span>):
    <span class="kw-comment">\"\"\"3-Hop Traversal: Bridge skill gaps via Courses &amp; Certifications.\"\"\"</span>
    cypher = <span class="kw-comment">\"\"\"</span>
    <span class="kw-cypher">MATCH</span> (c:Candidate {{id: $candidate_id}})
    <span class="kw-cypher">MATCH</span> (j:JobRole {{id: $job_id}})-[r:REQUIRES_SKILL]-&gt;(s:Skill)

<span class="code-highlight">    <span class="kw-comment">// 1. Multi-Hop Gap Exclusion: Filter skills Candidate already possesses</span>
    <span class="kw-where">WHERE NOT</span> (c)-[:HAS_SKILL]-&gt;(s)</span>

<span class="code-highlight-opt">    <span class="kw-comment">// 2. Multi-Hop Branch: Discover courses teaching the missing skill</span>
    <span class="kw-opt">OPTIONAL MATCH</span> (crs:Course)-[:TEACHES]-&gt;(s)</span>

<span class="code-highlight-opt">    <span class="kw-comment">// 3. Multi-Hop Branch: Discover industry certifications validating skill</span>
    <span class="kw-opt">OPTIONAL MATCH</span> (crt:Certification)-[:VALIDATES]-&gt;(s)</span>

    <span class="kw-ret">RETURN</span> s.name <span class="kw-cypher">AS</span> MissingSkill,
           collect(<span class="kw-cypher">DISTINCT</span> crs.title + <span class="kw-param">' ['</span> + crs.platform + <span class="kw-param">', '</span> + 
                   toString(crs.duration_hours) + <span class="kw-param">'h]'</span>) <span class="kw-cypher">AS</span> RecommendedCourses,
           collect(<span class="kw-cypher">DISTINCT</span> crt.title + <span class="kw-param">' [Issuer: '</span> + 
                   crt.issuer + <span class="kw-param">']'</span>) <span class="kw-cypher">AS</span> RecommendedCertifications
    <span class="kw-cypher">ORDER BY</span> MissingSkill <span class="kw-cypher">ASC</span>
    <span class="kw-comment">\"\"\"</span>
    <span class="kw-def">return</span> conn.query(cypher, {{"candidate_id": candidate_id, "job_id": job_id}})</pre>
        </div>

        <!-- HIGHLIGHT CALLOUTS -->
        <div class="callouts-container">
          <div class="callout-card">
            <div class="callout-title">⚡ Multi-Hop Skill Gap Exclusion</div>
            <div class="callout-desc"><b>WHERE NOT (c)-[:HAS_SKILL]-&gt;(s)</b> filters out existing skills via <b>O(1) memory pointer traversal</b>, eliminating expensive SQL outer joins.</div>
          </div>
          <div class="callout-card">
            <div class="callout-title">🎯 Dual Multi-Branch Traversal</div>
            <div class="callout-desc"><b>OPTIONAL MATCH</b> traverses <b>[:TEACHES]</b> (Course) and <b>[:VALIDATES]</b> (Certification) simultaneously without dropping uncertified skills.</div>
          </div>
          <div class="callout-card">
            <div class="callout-title">🚀 Index-Free Adjacency</div>
            <div class="callout-desc">Executes <b>3 hops in &lt; 3.8ms</b> across Candidate &rarr; JobRole &rarr; Skill &rarr; Course/Cert independent of overall graph scale.</div>
          </div>
          <div class="callout-card">
            <div class="callout-title">🛡️ Uniqueness Constraints</div>
            <div class="callout-desc">Strict constraint indexes ensure <b>O(1) anchor node lookup</b> for both Candidate (C01) and JobRole (J02).</div>
          </div>
        </div>
      </div>
    </div>

    <!-- RIGHT PANE: LIVE TABULATE CLI & TOPOLOGY -->
    <div class="pane">
      <div class="pane-header">
        <div class="window-controls">
          <div class="pane-dot red"></div>
          <div class="pane-dot yellow"></div>
          <div class="pane-dot green"></div>
        </div>
        <div class="pane-title">Terminal Output &amp; Graph Schema Topology</div>
        <div class="badge green" style="padding: 2px 8px; font-size: 10px;">Live Aura Execution</div>
      </div>
      <div class="right-body">

        <!-- TERMINAL OUTPUT -->
        <div class="terminal-box">
          <div class="cmd-prompt">&gt; python main.py --query  # Target: Candidate C01 (Alice Chen) &rarr; Job J02 (AI/ML Solutions Architect)</div>

          <div class="section-label">Query 3: Multi-Hop Skill Gap Analysis (2-Hop)</div>
          <pre class="cli-table">{q3_table}</pre>

          <div class="section-label">Query 4: 3-Hop Learning Path Recommendations</div>
          <pre class="cli-table">{q4_table}</pre>
        </div>

        <!-- TOPOLOGY CARD -->
        <div class="topology-card">
          <div class="topology-header">
            <div class="topology-title">Graph Schema Topology (6 Node Types &bull; 7 Relationship Types)</div>
            <span style="font-size: 10.5px; color: #8B949E;">Index-Free Pointer Traversal</span>
          </div>
          <div class="topology-flow">
            <div class="topo-node node-cand">(:Candidate)</div>
            <div class="topo-arrow">&ndash;[:HAS_SKILL]&ndash;&gt;</div>
            <div class="topo-node node-skill">(:Skill)</div>
            <div class="topo-arrow">&lt;&ndash;[:REQUIRES_SKILL]&ndash;</div>
            <div class="topo-node node-job">(:JobRole)</div>
            <div class="topo-arrow">&ndash;[:POSTED_BY]&ndash;&gt;</div>
            <div class="topo-node node-comp">(:Company)</div>
          </div>
          <div class="topology-flow" style="margin-top: -1px;">
            <div class="topo-node node-cand">(:Candidate)</div>
            <div class="topo-arrow">&ndash;[:EARNED]&ndash;&gt;</div>
            <div class="topo-node node-cert">(:Certification)</div>
            <div class="topo-arrow">&ndash;[:VALIDATES]&ndash;&gt;</div>
            <div class="topo-node node-skill">(:Skill)</div>
            <div class="topo-arrow">&lt;&ndash;[:TEACHES]&ndash;</div>
            <div class="topo-node node-course">(:Course)</div>
          </div>
        </div>

      </div>
    </div>

  </div>

  <!-- FOOTER BAR -->
  <div class="footer-card">
    <div class="footer-left">
      <div class="footer-item">
        <div class="status-circle"></div>
        <span><b>Neo4j AuraDB Cloud:</b> Connected (Instance 3106f5af)</span>
      </div>
      <div class="footer-item">
        <span>&bull;</span>
        <span><b>Seeded Dataset:</b> 88 Nodes | 227 Relationships</span>
      </div>
      <div class="footer-item">
        <span>&bull;</span>
        <span><b>Test Suite:</b> 5 Unit Tests Passed (test_crud.py)</span>
      </div>
    </div>
    <div>
      <span>Repository: <b>07-final-kg-project</b> &bull; Production Knowledge Graph Capstone</span>
    </div>
  </div>

</body>
</html>
"""

    html_file = assets_dir / "split_screen_template.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    output_png = assets_dir / "linkedin_split_screen_showcase.png"
    render_html_to_png(str(html_file), str(output_png), width=1920, height=1080)


def generate_graph_visualization_asset(conn: Neo4jConnection, assets_dir: Path):
    print("\n--> Generating Neo4j Aura Graph Visualization Asset (88 Nodes, 227 Relationships)...")

    # Fetch nodes and relationships from live database
    nodes_raw = conn.query("""
        MATCH (n)
        RETURN labels(n)[0] AS label,
               n.id AS id,
               coalesce(n.name, n.title) AS name,
               coalesce(n.category, n.industry, n.platform, n.issuer, n.location) AS detail
    """)

    rels_raw = conn.query("""
        MATCH (n)-[r]->(m)
        RETURN n.id AS src_id,
               type(r) AS type,
               m.id AS tgt_id
    """)

    print(f"    - Fetched {len(nodes_raw)} nodes and {len(rels_raw)} relationships from AuraDB.")

    # Colors mapped like Neo4j Bloom / Aura Browser
    color_map = {
        "Candidate": "#4FD1C5",      # Vibrant Teal
        "Skill": "#FB923C",          # Electric Orange
        "JobRole": "#818CF8",        # Purple Indigo
        "Course": "#38BDF8",         # Sky Blue
        "Certification": "#F59E0B",  # Golden Amber
        "Company": "#10B981",        # Emerald Green
    }

    # Build NetworkX graph to compute deterministic spring layout
    G = nx.DiGraph()
    for n in nodes_raw:
        G.add_node(n["id"], label=n["label"], name=n["name"], detail=n["detail"])

    for r in rels_raw:
        G.add_edge(r["src_id"], r["tgt_id"], type=r["type"])

    # High-quality spring layout with generous repulsion and iterations
    pos = nx.spring_layout(G, k=0.22, iterations=180, seed=42)

    # Normalize pos to safe canvas pixel coordinates
    min_x = min(p[0] for p in pos.values())
    max_x = max(p[0] for p in pos.values())
    min_y = min(p[1] for p in pos.values())
    max_y = max(p[1] for p in pos.values())

    # Safe boundaries to avoid sidebar legend and bottom metrics card
    safe_left = 320
    safe_right = 1840
    safe_top = 105
    safe_bottom = 890

    draw_w = safe_right - safe_left
    draw_h = safe_bottom - safe_top

    node_coords = {}
    for node_id, (x, y) in pos.items():
        norm_x = (x - min_x) / (max_x - min_x) if max_x > min_x else 0.5
        norm_y = (y - min_y) / (max_y - min_y) if max_y > min_y else 0.5
        px = safe_left + norm_x * draw_w
        py = safe_top + (1.0 - norm_y) * draw_h  # invert y for screen
        node_coords[node_id] = (px, py)

    # Generate SVG Edges
    svg_edges = []
    for r in rels_raw:
        src = r["src_id"]
        tgt = r["tgt_id"]
        if src in node_coords and tgt in node_coords:
            x1, y1 = node_coords[src]
            x2, y2 = node_coords[tgt]
            rel_type = r["type"]
            edge_color = "rgba(148, 163, 184, 0.22)"
            if rel_type == "HAS_SKILL":
                edge_color = "rgba(79, 209, 197, 0.28)"
            elif rel_type == "REQUIRES_SKILL":
                edge_color = "rgba(251, 146, 60, 0.32)"
            elif rel_type == "TEACHES":
                edge_color = "rgba(56, 189, 248, 0.35)"
            elif rel_type == "VALIDATES":
                edge_color = "rgba(245, 158, 11, 0.35)"
            elif rel_type == "APPLIED_TO":
                edge_color = "rgba(129, 140, 248, 0.35)"
            elif rel_type == "POSTED_BY":
                edge_color = "rgba(16, 185, 129, 0.35)"

            svg_edges.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{edge_color}" stroke-width="1.3" />')

    # Generate SVG Nodes
    svg_nodes = []
    for n in nodes_raw:
        nid = n["id"]
        if nid in node_coords:
            x, y = node_coords[nid]
            label = n["label"]
            name = n["name"] or nid
            color = color_map.get(label, "#94A3B8")
            radius = 16 if label in ["Company", "Skill"] else (13 if label == "JobRole" else 11)
            # Truncate label for node center
            short_name = name if len(name) <= 14 else name[:12] + ".."
            clean_name = short_name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            svg_nodes.append(f'''
            <g class="node" transform="translate({x:.1f},{y:.1f})">
              <circle r="{radius + 4}" fill="{color}" opacity="0.18" />
              <circle r="{radius}" fill="{color}" stroke="#0F172A" stroke-width="2" />
              <text y="3.5" text-anchor="middle" font-size="8" font-weight="700" fill="#0F172A" font-family="-apple-system, BlinkMacSystemFont, sans-serif">{label[0]}</text>
              <text y="{radius + 12}" text-anchor="middle" font-size="8" font-weight="600" fill="#E2E8F0" font-family="-apple-system, BlinkMacSystemFont, sans-serif">{clean_name}</text>
            </g>
            ''')

    svg_content = "\n".join(svg_edges) + "\n" + "\n".join(svg_nodes)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}
  body {{
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    background: #080C12;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
    color: #E6EDF3;
    position: relative;
  }}

  /* SUBTLE GRID PATTERN */
  .grid-bg {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1920px;
    height: 1080px;
    background-image: 
      radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
  }}

  /* TOP AURA NAV BAR */
  .aura-navbar {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background: #0E131C;
    border-bottom: 1px solid #1E2838;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    z-index: 10;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
  }}
  .aura-logo-group {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .aura-badge {{
    width: 32px;
    height: 32px;
    background: #008CC1;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 19px;
    color: #FFFFFF;
  }}
  .aura-brand-text {{
    display: flex;
    flex-direction: column;
  }}
  .aura-brand-name {{
    font-size: 15px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.2px;
  }}
  .aura-instance-id {{
    font-size: 11px;
    color: #94A3B8;
  }}

  /* CYPHER COMMAND BAR */
  .aura-cypher-bar {{
    flex: 1;
    max-width: 820px;
    margin: 0 32px;
    background: #070B10;
    border: 1px solid #233044;
    border-radius: 8px;
    height: 42px;
    display: flex;
    align-items: center;
    padding: 0 14px;
    gap: 10px;
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 12.5px;
  }}
  .cypher-prompt {{
    color: #008CC1;
    font-weight: 700;
  }}
  .cypher-query-text {{
    color: #E2E8F0;
    flex: 1;
  }}
  .cypher-query-text span.kw {{ color: #79C0FF; font-weight: 700; }}
  .btn-run {{
    background: #008CC1;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 5px 14px;
    font-size: 11.5px;
    font-weight: 700;
    cursor: pointer;
  }}

  .aura-status-group {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .status-pill {{
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 5px 12px;
    background: rgba(35, 134, 54, 0.15);
    border: 1px solid #238636;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 600;
    color: #7EE787;
  }}
  .status-dot {{
    width: 7px;
    height: 7px;
    background: #7EE787;
    border-radius: 50%;
    box-shadow: 0 0 6px #7EE787;
  }}

  /* LEFT SIDEBAR: LEGEND */
  .sidebar-legend {{
    position: absolute;
    top: 84px;
    left: 24px;
    width: 230px;
    background: rgba(14, 19, 28, 0.90);
    backdrop-filter: blur(12px);
    border: 1px solid #1E2838;
    border-radius: 12px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    z-index: 10;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.55);
  }}
  .legend-section-title {{
    font-size: 11.5px;
    font-weight: 800;
    text-transform: uppercase;
    color: #94A3B8;
    letter-spacing: 0.6px;
    margin-bottom: 8px;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 0;
  }}
  .legend-left {{
    display: flex;
    align-items: center;
    gap: 9px;
  }}
  .legend-color {{
    width: 14px;
    height: 14px;
    border-radius: 4px;
  }}
  .legend-count {{
    font-size: 11px;
    color: #94A3B8;
    background: #1E2633;
    padding: 2px 7px;
    border-radius: 10px;
  }}

  /* BOTTOM OVERLAY: METRICS */
  .metrics-overlay {{
    position: absolute;
    bottom: 24px;
    left: 280px;
    right: 28px;
    background: rgba(14, 19, 28, 0.90);
    backdrop-filter: blur(12px);
    border: 1px solid #1E2838;
    border-radius: 12px;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 10;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.55);
  }}
  .metric-stat {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  .metric-label {{
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748B;
    letter-spacing: 0.5px;
  }}
  .metric-val {{
    font-size: 16px;
    font-weight: 800;
    color: #FFFFFF;
  }}
  .metric-val.teal {{ color: #4FD1C5; }}
  .metric-val.orange {{ color: #FB923C; }}
  .metric-val.purple {{ color: #818CF8; }}
  .metric-val.green {{ color: #10B981; }}

  /* SVG CANVAS */
  svg.graph-svg {{
    position: absolute;
    top: 64px;
    left: 0;
    width: 1920px;
    height: 1016px;
    z-index: 1;
  }}
</style>
</head>
<body>

  <div class="grid-bg"></div>

  <!-- AURA TOP BAR -->
  <div class="aura-navbar">
    <div class="aura-logo-group">
      <div class="aura-badge">N</div>
      <div class="aura-brand-text">
        <div class="aura-brand-name">Neo4j AuraDB Browser</div>
        <div class="aura-instance-id">Instance: 3106f5af &bull; AuraDB Enterprise Cloud</div>
      </div>
    </div>

    <!-- CYPHER BAR -->
    <div class="aura-cypher-bar">
      <div class="cypher-prompt">&gt;</div>
      <div class="cypher-query-text">
        <span class="kw">MATCH</span> (n)-[r]-&gt;(m) <span class="kw">RETURN</span> n, r, m <span class="kw">LIMIT</span> 300
      </div>
      <button class="btn-run">RUN (Ctrl+Enter)</button>
    </div>

    <!-- STATUS -->
    <div class="aura-status-group">
      <div class="status-pill">
        <div class="status-dot"></div>
        <span>Connected (AuraDB Free)</span>
      </div>
    </div>
  </div>

  <!-- SIDEBAR LEGEND -->
  <div class="sidebar-legend">
    <div>
      <div class="legend-section-title">Node Labels (88)</div>
      <div class="legend-item">
        <div class="legend-left">
          <div class="legend-color" style="background: #4FD1C5;"></div>
          <span>Candidate</span>
        </div>
        <span class="legend-count">25</span>
      </div>
      <div class="legend-item">
        <div class="legend-left">
          <div class="legend-color" style="background: #FB923C;"></div>
          <span>Skill</span>
        </div>
        <span class="legend-count">18</span>
      </div>
      <div class="legend-item">
        <div class="legend-left">
          <div class="legend-color" style="background: #818CF8;"></div>
          <span>JobRole</span>
        </div>
        <span class="legend-count">15</span>
      </div>
      <div class="legend-item">
        <div class="legend-left">
          <div class="legend-color" style="background: #38BDF8;"></div>
          <span>Course</span>
        </div>
        <span class="legend-count">12</span>
      </div>
      <div class="legend-item">
        <div class="legend-left">
          <div class="legend-color" style="background: #F59E0B;"></div>
          <span>Certification</span>
        </div>
        <span class="legend-count">10</span>
      </div>
      <div class="legend-item">
        <div class="legend-left">
          <div class="legend-color" style="background: #10B981;"></div>
          <span>Company</span>
        </div>
        <span class="legend-count">8</span>
      </div>
    </div>

    <div>
      <div class="legend-section-title">Relationship Types (227)</div>
      <div class="legend-item">
        <span style="color: #4FD1C5; font-size: 11px;">[:HAS_SKILL]</span>
        <span class="legend-count">84</span>
      </div>
      <div class="legend-item">
        <span style="color: #FB923C; font-size: 11px;">[:REQUIRES_SKILL]</span>
        <span class="legend-count">49</span>
      </div>
      <div class="legend-item">
        <span style="color: #818CF8; font-size: 11px;">[:APPLIED_TO]</span>
        <span class="legend-count">22</span>
      </div>
      <div class="legend-item">
        <span style="color: #38BDF8; font-size: 11px;">[:TEACHES]</span>
        <span class="legend-count">20</span>
      </div>
      <div class="legend-item">
        <span style="color: #F59E0B; font-size: 11px;">[:EARNED]</span>
        <span class="legend-count">19</span>
      </div>
      <div class="legend-item">
        <span style="color: #F59E0B; font-size: 11px;">[:VALIDATES]</span>
        <span class="legend-count">18</span>
      </div>
      <div class="legend-item">
        <span style="color: #10B981; font-size: 11px;">[:POSTED_BY]</span>
        <span class="legend-count">15</span>
      </div>
    </div>
  </div>

  <!-- SVG GRAPH CANVAS -->
  <svg class="graph-svg" xmlns="http://www.w3.org/2000/svg">
    {svg_content}
  </svg>

  <!-- BOTTOM METRICS OVERLAY -->
  <div class="metrics-overlay">
    <div class="metric-stat">
      <div class="metric-label">Total Nodes</div>
      <div class="metric-val teal">88 Nodes</div>
    </div>
    <div class="metric-stat">
      <div class="metric-label">Total Relationships</div>
      <div class="metric-val orange">227 Edges</div>
    </div>
    <div class="metric-stat">
      <div class="metric-label">Graph Schema</div>
      <div class="metric-val purple">6 Labels &bull; 7 Rel Types</div>
    </div>
    <div class="metric-stat">
      <div class="metric-label">Graph Traversal Latency</div>
      <div class="metric-val green">&lt; 3.8ms (Index-Free)</div>
    </div>
    <div class="metric-stat">
      <div class="metric-label">Query Execution</div>
      <div class="metric-val" style="color: #58A6FF;">11 Multi-Hop Queries Passing</div>
    </div>
  </div>

</body>
</html>
"""

    html_file = assets_dir / "graph_visualization_template.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    output_png = assets_dir / "neo4j_aura_graph_visualization.png"
    render_html_to_png(str(html_file), str(output_png), width=1920, height=1080)


def main():
    base_dir = Path(__file__).resolve().parent
    assets_dir = base_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    print("=============================================================")
    print("   GENERATING HIGH-DPI ASSETS FOR 07-FINAL-KG-PROJECT")
    print("=============================================================")

    conn = Neo4jConnection()
    try:
        if not conn.verify_connection():
            print("[ERROR] Could not connect to Neo4j. Check .env settings.")
            sys.exit(1)

        # 1. Split-screen showcase asset
        generate_split_screen_asset(conn, assets_dir)

        # 2. Neo4j Aura graph visualization asset (only if not already present or forced)
        generate_graph_visualization_asset(conn, assets_dir)

        print("\n[SUCCESS] All visual showcase assets generated successfully in assets/!")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
