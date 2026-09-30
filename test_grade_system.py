import unittest
from pathlib import Path

from grade_system import GradeSystem


class GradeSystemTests(unittest.TestCase):
    def setUp(self):
        self.data_file = Path(__file__).parent / "_test_students.json"
        self.data_file.unlink(missing_ok=True)
        self.system = GradeSystem(self.data_file)

    def tearDown(self):
        self.data_file.unlink(missing_ok=True)

    def test_calculates_average_and_letter_grade(self):
        self.system.add_student("S001", "Ada Lovelace")
        self.system.record_grade("S001", "Math", 95)
        self.system.record_grade("S001", "Science", 85)
        student = self.system.report("S001")
        self.assertEqual(student.average, 90)
        self.assertEqual(student.letter_grade, "A+")

    def test_persists_students(self):
        self.system.add_student("S002", "Grace Hopper")
        self.system.record_grade("S002", "Programming", 78)
        restored = GradeSystem(self.data_file)
        self.assertEqual(restored.report("S002").name, "Grace Hopper")
        self.assertEqual(restored.report("S002").letter_grade, "B")

    def test_rejects_invalid_score(self):
        self.system.add_student("S003", "Linus Torvalds")
        with self.assertRaises(ValueError):
            self.system.record_grade("S003", "Systems", 101)


if __name__ == "__main__":
    unittest.main()
