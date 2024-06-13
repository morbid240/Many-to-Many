from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKeyConstraint
from typing import List 


class Enrollment(Base):
    """Association class between students and sections."""
    __tablename__ = "enrollments"  # Give SQLAlchemy th name of the table.
    # Primary keys - all migrating foreign keys I guess...
    studentID: Mapped[int] = mapped_column('student_id', primary_key=True)
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', primary_key=True)
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer, nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True)
    # Define relationships 
    section: Mapped["Section"] = relationship(back_populates="students")  
    student: Mapped["Student"] = relationship(back_populates="sections") 
    # FK constraint makes sure that no student enrolls in the same course more than once the same semester
    __table_args__ = (
        ForeignKeyConstraint([departmentAbbreviation, courseNumber, sectionYear, semester, studentID], 
                             [section.departmentAbbreviation, section.courseNumber, section.semester, student.studentID])
    )

    def __init__(self, section, student):
        self.set_section(section)
        self.set_student(section)
    # get stuff from classes
    def set_student(self, student):
        self.student = student
        self.studentID = student.studentID
    def set_section(self, section):
        self.section = section
        self.departmentAbbreviation = section.departmentAbbreviation
        self.courseNumber = section.courseNumber
        self.sectionNumber = section.sectionNumber
        self.semester = section.semester
        self.sectionYear = section.sectionYear

    def __str__(self):
        return f"Student {self.student} enrolled in section: {self.section}"

