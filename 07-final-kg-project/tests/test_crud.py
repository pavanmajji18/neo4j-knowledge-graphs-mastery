"""
Unit tests for CRUD operations on the Neo4j Knowledge Graph.
"""
import sys
import unittest
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.connection import Neo4jConnection
from src.crud import (
    create_candidate,
    get_candidate_by_id,
    update_candidate_experience,
    add_candidate_skill,
    remove_candidate_skill,
    delete_candidate,
)


class TestNeo4jCRUD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = Neo4jConnection()
        cls.test_candidate_id = "TEST_C100"

    @classmethod
    def tearDownClass(cls):
        # Cleanup test candidate
        delete_candidate(cls.conn, cls.test_candidate_id)
        cls.conn.close()

    def test_01_create_candidate(self):
        result = create_candidate(
            self.conn,
            candidate_id=self.test_candidate_id,
            name="Unit Test Candidate",
            experience_yrs=4,
            location="Test City",
            email="unittest@example.com"
        )
        self.assertEqual(result["id"], self.test_candidate_id)
        self.assertEqual(result["name"], "Unit Test Candidate")
        self.assertEqual(result["experience_yrs"], 4)

    def test_02_get_candidate_by_id(self):
        profile = get_candidate_by_id(self.conn, self.test_candidate_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile["id"], self.test_candidate_id)
        self.assertEqual(profile["email"], "unittest@example.com")

    def test_03_update_candidate_experience(self):
        updated = update_candidate_experience(self.conn, self.test_candidate_id, 5)
        self.assertEqual(updated["experience_yrs"], 5)

    def test_04_add_and_remove_skill(self):
        # Add S01 (Neo4j)
        link = add_candidate_skill(self.conn, self.test_candidate_id, "S01", "Expert", 3)
        self.assertEqual(link["proficiency"], "Expert")

        profile = get_candidate_by_id(self.conn, self.test_candidate_id)
        skill_ids = [s["id"] for s in profile["skills"]]
        self.assertIn("S01", skill_ids)

        # Remove S01
        removed = remove_candidate_skill(self.conn, self.test_candidate_id, "S01")
        self.assertTrue(removed)

    def test_05_delete_candidate(self):
        deleted = delete_candidate(self.conn, self.test_candidate_id)
        self.assertTrue(deleted)
        profile = get_candidate_by_id(self.conn, self.test_candidate_id)
        self.assertIsNone(profile)


if __name__ == "__main__":
    unittest.main()
