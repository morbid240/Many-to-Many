from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKeyConstraint
from typing import List 


class Enrollment(Base):
    __tablename__ = "enrollments"  # Give SQLAlchemy th name of the table.
    # Primary keys - all migrating foreign keys I guess...
    """Primary keys:{student_id, department_abbreviation, course_number, section_number, section_year, semester} """
    studentID: Mapped[int}: Mapped[int] = mapped_column('student_id', primary_key=True)
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', primary_key=True)
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer, nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True)
    # Define relationships 
    students: Mapped[List["Student"]] = relationship(back_populates="enrollments")  
    sections: Mapped[List["Section"]] = relationship(back_populates="enrollments") 

    # FK constraint makes sure that no student enrolls in the same course more than once the same semester
    __table_args__ = (
        ForeignKeyConstraint([departmentAbbreviation, courseNumber, sectionYear, semester, studentID], 
                             [Section.departmentAbbreviation, Section.courseNumber, Section.semester, Student.studentID])
    )

    def __init__(self, section: Section, student: Student):
        self.set_section(section)
        self.set_student(section)
            
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
