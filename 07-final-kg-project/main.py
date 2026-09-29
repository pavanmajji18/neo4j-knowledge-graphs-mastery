"""
Main CLI Application Runner for Neo4j Job & Skill Recommendation Knowledge Graph.
Provides an interactive menu for database seeding, CRUD operations, and multi-hop Cypher queries.
"""
import sys
import argparse
from pathlib import Path
from tabulate import tabulate

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.connection import Neo4jConnection
from src.seed_data import seed_database, verify_summary
from src import crud
from src import queries


def print_banner():
    print("""
====================================================================
   NEO4J KNOWLEDGE GRAPH: JOB & SKILL RECOMMENDATION ENGINE
====================================================================
  Node Types        : Candidate, Skill, JobRole, Company, Certification, Course (6 Types)
  Relationship Types: HAS_SKILL, APPLIED_TO, REQUIRES_SKILL, POSTED_BY,
                      TEACHES, EARNED, VALIDATES (7 Types)
====================================================================
    """)


def menu_seed_db(conn: Neo4jConnection):
    print("\n[Action] Re-seeding Neo4j Database...")
    seed_database(conn, wipe_existing=True)


def menu_run_all_queries(conn: Neo4jConnection):
    print("\n[Action] Executing 11 Analytical Cypher Queries...")
    queries.run_all_queries(conn)


def menu_crud_demo(conn: Neo4jConnection):
    print("\n--- Interactive CRUD Operations Demo ---")
    candidate_id = "C_DEMO01"

    # 1. Create Candidate
    print("\n1. [CREATE] Inserting new Candidate 'Jordan Lee' (id: C_DEMO01)...")
    new_c = crud.create_candidate(
        conn,
        candidate_id=candidate_id,
        name="Jordan Lee",
        experience_yrs=4,
        location="San Francisco, CA",
        email="jordan.lee@example.com"
    )
    print("   Inserted:", new_c)

    # Add Skills
    print("\n   [LINK] Adding skills S01 (Neo4j) and S03 (Python) to Jordan Lee...")
    crud.add_candidate_skill(conn, candidate_id, "S01", proficiency="Expert", years=3)
    crud.add_candidate_skill(conn, candidate_id, "S03", proficiency="Expert", years=4)

    # 2. Read Candidate
    print(f"\n2. [READ] Fetching Candidate Profile for '{candidate_id}'...")
    profile = crud.get_candidate_by_id(conn, candidate_id)
    if profile:
        print(f"   Name      : {profile.get('name')}")
        print(f"   Experience: {profile.get('experience_yrs')} yrs")
        print(f"   Location  : {profile.get('location')}")
        print(f"   Skills    : {[s['name'] + ' (' + s['proficiency'] + ')' for s in profile.get('skills', [])]}")

    # 3. Update Candidate
    print(f"\n3. [UPDATE] Updating experience for '{candidate_id}' to 5 years...")
    updated = crud.update_candidate_experience(conn, candidate_id, 5)
    print("   Updated Node:", updated)

    # 4. Delete Candidate
    print(f"\n4. [DELETE] Detaching and Deleting Candidate '{candidate_id}'...")
    deleted = crud.delete_candidate(conn, candidate_id)
    print(f"   Deleted Successfully: {deleted}")


def menu_skill_gap_demo(conn: Neo4jConnection):
    print("\n--- Multi-Hop Skill Gap & Learning Path Analysis ---")
    candidate_id = input("Enter Candidate ID [Default: C01]: ").strip() or "C01"
    job_id = input("Enter Target Job Role ID [Default: J02]: ").strip() or "J02"

    print(f"\nSearching missing skills for Candidate '{candidate_id}' targeting Job '{job_id}'...")
    gaps = queries.q3_skill_gap_analysis(conn, candidate_id, job_id)
    if gaps:
        print("\nMissing Skills:")
        print(tabulate(gaps, headers="keys", tablefmt="grid"))
    else:
        print("No missing skills found! Candidate meets all skill requirements.")

    print(f"\n3-Hop Learning Path Recommendations for '{candidate_id}':")
    recs = queries.q4_learning_path_recommendations(conn, candidate_id, job_id)
    if recs:
        print(tabulate(recs, headers="keys", tablefmt="grid"))


def main_interactive():
    print_banner()
    conn = Neo4jConnection()

    if not conn.verify_connection():
        print("[ERROR] Could not connect to Neo4j database. Check .env settings.")
        sys.exit(1)

    while True:
        print("\nMain Menu Options:")
        print("  1. Seed / Reset Database (88 Nodes, 227 Rels)")
        print("  2. Run All 11 Analytical Cypher Queries (Multi-Hop Traversals & Analytics)")
        print("  3. Run Interactive CRUD Operations Demo")
        print("  4. Skill Gap & Learning Path Recommendation Tool")
        print("  5. Display Graph Dataset Summary")
        print("  0. Exit")

        choice = input("\nSelect Option [0-5]: ").strip()

        if choice == "1":
            menu_seed_db(conn)
        elif choice == "2":
            menu_run_all_queries(conn)
        elif choice == "3":
            menu_crud_demo(conn)
        elif choice == "4":
            menu_skill_gap_demo(conn)
        elif choice == "5":
            verify_summary(conn)
        elif choice == "0":
            print("Exiting application. Goodbye!")
            conn.close()
            break
        else:
            print("Invalid option. Please choose 0-5.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Neo4j Knowledge Graph CLI Runner")
    parser.add_argument("--seed", action="store_true", help="Seed database and exit")
    parser.add_argument("--query", action="store_true", help="Run all queries and exit")
    parser.add_argument("--crud", action="store_true", help="Run CRUD demo and exit")
    args = parser.parse_args()

    conn = Neo4jConnection()
    try:
        if args.seed:
            seed_database(conn, wipe_existing=True)
        elif args.query:
            queries.run_all_queries(conn)
        elif args.crud:
            menu_crud_demo(conn)
        else:
            main_interactive()
    finally:
        conn.close()
