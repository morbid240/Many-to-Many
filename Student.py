"""
Malcolm Roddy
CECS 323
Many to Many SQL
Due Date: 06/14/2024

Only stuff added here: 
    -import Enrollment assoication class
    -new relationship between student and section
    -methods for adding/removing sections from the student
Everything else remains unchanged (I think)
"""

from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from StudentMajor import StudentMajor
from datetime import datetime

from Enrollment import Enrollment

class Student(Base):
    """An individual who may or may not be enrolled at the university, who
    enrolls in courses toward some educational objective. That objective
    could be a formal degree program, or it could be a specialized certificate."""
    __tablename__ = "students"
    # Let SQLAlchemy handle the generation of student_id values for us.
    studentID: Mapped[int] = mapped_column('student_id', Integer, Identity(start=1, cycle=True), primary_key=True)
    lastName: Mapped[str] = mapped_column('last_name', String(50), nullable=False, primary_key=False)
    firstName: Mapped[str] = mapped_column('first_name', String(50), nullable=False, primary_key=False)
    email: Mapped[str] = mapped_column('email', String(255), nullable=False)
    
    # Relationships
    majors: Mapped[List["StudentMajor"]] = relationship(
        "StudentMajor", back_populates="student", cascade="all, save-update, delete-orphan"
    )
    sections: Mapped[List["Enrollment"]] = relationship(
        "Enrollment", back_populates="student", cascade="all, save-update, delete-orphan"
    )

    #Constraints
    __table_args__ = (
        UniqueConstraint("first_name", "last_name", name="students_uk_01"),
        UniqueConstraint("email", name="students_uk_02")
    )

    def __init__(self, lastName: str, firstName: str, email: str):
        self.lastName = lastName
        self.firstName = firstName
        self.email = email

    # add/remove sections in student list
    def add_section(self, section):
        """Add a section to a list of sections the student is enrolled in currently."""
        for next_section in self.sections:
            if next_section.section == section:
                return  # Student already enrolled in section
        student_enrollment = Enrollment(section, self)
        section.students.append(student_enrollment)
        self.sections.append(student_enrollment)

    
    def remove_section(self, section):
        """Remove a section from the list of sections the student is enrolled in."""
        for next_section in self.sections:
            if next_section.section == section:
                self.sections.remove(next_section)
                return

    
    def add_major(self, major):
        """Add a new major to the student."""
        for next_major in self.majors:
            if next_major.major == major:
                return  # This student already has this major
        student_major = StudentMajor(self, major, datetime.now())
        self.majors.append(student_major)

    
    def remove_major(self, major):
        """Remove a major from the list of majors that a student presently has declared."""
        for next_major in self.majors:
            if next_major.major == major:
                self.majors.remove(next_major)
                return

    
    def __str__(self):
        return f"Student ID: {self.student_id} name: {self.last_name}, {self.first_name} e-mail: {self.email}"
