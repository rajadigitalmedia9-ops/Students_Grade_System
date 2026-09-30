"""A small, persistent command-line student grade system."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


GRADE_SCALE = ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (0, "F"))


@dataclass
class Student:
    student_id: str
    name: str
    grades: dict[str, float] = field(default_factory=dict)

    @property
    def average(self) -> float:
        return sum(self.grades.values()) / len(self.grades) if self.grades else 0.0

    @property
    def letter_grade(self) -> str:
        return next(letter for minimum, letter in GRADE_SCALE if self.average >= minimum)


class GradeSystem:
    def __init__(self, data_file: str | Path = "students.json") -> None:
        self.data_file = Path(data_file)
        self.students: dict[str, Student] = {}
        self.load()

    def add_student(self, student_id: str, name: str) -> Student:
        student_id, name = student_id.strip(), name.strip()
        if not student_id or not name:
            raise ValueError("Student ID and name are required.")
        if student_id in self.students:
            raise ValueError("A student with that ID already exists.")
        student = Student(student_id, name)
        self.students[student_id] = student
        self.save()
        return student

    def record_grade(self, student_id: str, subject: str, score: float) -> None:
        if student_id not in self.students:
            raise ValueError("Student not found.")
        subject = subject.strip()
        if not subject:
            raise ValueError("Subject is required.")
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100.")
        self.students[student_id].grades[subject] = score
        self.save()

    def report(self, student_id: str) -> Student:
        try:
            return self.students[student_id]
        except KeyError as error:
            raise ValueError("Student not found.") from error

    def list_students(self) -> list[Student]:
        return sorted(self.students.values(), key=lambda student: student.name.lower())

    def save(self) -> None:
        payload = [asdict(student) for student in self.students.values()]
        self.data_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> None:
        if not self.data_file.exists():
            return
        records = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.students = {record["student_id"]: Student(**record) for record in records}


def display_report(student: Student) -> None:
    print(f"\nReport: {student.name} ({student.student_id})")
    if not student.grades:
        print("No grades recorded.")
        return
    for subject, score in sorted(student.grades.items()):
        print(f"  {subject}: {score:.1f}")
    print(f"Average: {student.average:.2f} | Final grade: {student.letter_grade}")


def main() -> None:
    system = GradeSystem()
    actions = "1. Add student  2. Record grade  3. Student report  4. List students  5. Exit"
    while True:
        print(f"\n{actions}")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                system.add_student(input("Student ID: "), input("Student name: "))
                print("Student added.")
            elif choice == "2":
                system.record_grade(input("Student ID: "), input("Subject: "), float(input("Score (0-100): ")))
                print("Grade saved.")
            elif choice == "3":
                display_report(system.report(input("Student ID: ").strip()))
            elif choice == "4":
                for student in system.list_students():
                    print(f"{student.student_id} | {student.name} | {student.average:.2f} ({student.letter_grade})")
            elif choice == "5":
                print("Goodbye!")
                return
            else:
                print("Please choose a number from 1 to 5.")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
