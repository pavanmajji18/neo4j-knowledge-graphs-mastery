class StudentCourseCRUD:
    def __init__(self, driver):
        self.driver = driver

    # 1. CREATE NODE
    def create_student(self, name: str, age: int, city: str):
        query = """
        CREATE (s:Student {name: $name, age: $age, city: $city})
        RETURN s.name AS name, s.age AS age, s.city AS city
        """
        with self.driver.session() as session:
            record = session.run(query, name=name, age=age, city=city).single()
            return dict(record) if record else None

    def create_course(self, course_name: str, code: str):
        query = """
        MERGE (c:Course {code: $code})
        ON CREATE SET c.name = $course_name
        RETURN c.name AS name, c.code AS code
        """
        with self.driver.session() as session:
            record = session.run(query, course_name=course_name, code=code).single()
            return dict(record) if record else None

    # 2. CREATE RELATIONSHIP
    def enroll_student(self, student_name: str, course_code: str, semester: str):
        query = """
        MATCH (s:Student {name: $student_name})
        MATCH (c:Course {code: $course_code})
        MERGE (s)-[r:ENROLLED_IN {semester: $semester}]->(c)
        RETURN s.name AS student, type(r) AS relationship, r.semester AS semester, c.name AS course
        """
        with self.driver.session() as session:
            record = session.run(
                query,
                student_name=student_name,
                course_code=course_code,
                semester=semester
            ).single()
            return dict(record) if record else None

    # 3. READ NODES
    def get_all_students(self):
        query = """
        MATCH (s:Student)
        RETURN s.name AS name, s.age AS age, s.city AS city
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    # 4. SEARCH / FILTER
    def find_students_by_city(self, city: str):
        query = """
        MATCH (s:Student)
        WHERE s.city = $city
        RETURN s.name AS name, s.age AS age, s.city AS city
        """
        with self.driver.session() as session:
            result = session.run(query, city=city)
            return [dict(record) for record in result]

    # 5. UPDATE PROPERTIES
    def update_student_age(self, name: str, new_age: int):
        query = """
        MATCH (s:Student {name: $name})
        SET s.age = $new_age
        RETURN s.name AS name, s.age AS age, s.city AS city
        """
        with self.driver.session() as session:
            record = session.run(query, name=name, new_age=new_age).single()
            return dict(record) if record else None

    # 6. DELETE RELATIONSHIP
    def remove_enrollment(self, student_name: str, course_code: str):
        query = """
        MATCH (s:Student {name: $student_name})-[r:ENROLLED_IN]->(c:Course {code: $course_code})
        DELETE r
        RETURN count(r) AS deleted_count
        """
        with self.driver.session() as session:
            record = session.run(
                query,
                student_name=student_name,
                course_code=course_code
            ).single()
            return record["deleted_count"]

    # 7. DELETE NODE
    def delete_student(self, name: str):
        query = """
        MATCH (s:Student {name: $name})
        DETACH DELETE s
        RETURN count(s) AS deleted_count
        """
        with self.driver.session() as session:
            record = session.run(query, name=name).single()
            return record["deleted_count"]
