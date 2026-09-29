from connection import Neo4jConnection
from crud_operations import StudentCourseCRUD

def run_pipeline():
    conn = Neo4jConnection()
    conn.verify_connection()
    crud = StudentCourseCRUD(conn.driver)

    try:
        print("\n--- 1. Creating Nodes ---")
        student = crud.create_student("Alice Smith", 22, "Seattle")
        crud.create_course("Knowledge Graphs 101", "CS501")
        print(f"Created: {student}")

        print("\n--- 2. Creating Relationship ---")
        rel = crud.enroll_student("Alice Smith", "CS501", "Fall 2026")
        print(f"Relationship: {rel}")

        print("\n--- 3. Reading All Students ---")
        print(crud.get_all_students())

        print("\n--- 4. Filtering By City (Seattle) ---")
        print(crud.find_students_by_city("Seattle"))

        print("\n--- 5. Updating Properties ---")
        updated = crud.update_student_age("Alice Smith", 23)
        print(f"Updated Student: {updated}")

        print("\n--- 6. Deleting Relationship ---")
        deleted_rels = crud.remove_enrollment("Alice Smith", "CS501")
        print(f"Enrollments Removed: {deleted_rels}")

        print("\n--- 7. Deleting Node ---")
        deleted_nodes = crud.delete_student("Alice Smith")
        print(f"Nodes Removed: {deleted_nodes}")

    finally:
        conn.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    run_pipeline()