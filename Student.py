from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from datetime import datetime

class Student(Base):
    """An individual who may or may not be enrolled at the university, who
    enrolls in courses toward some educational objective. That objective
    could be a formal degree program, or it could be a specialized certificate."""
    
    __tablename__ = "students"
    
    # Let SQLAlchemy handle the generation of student_id values for us.
    student_id: Mapped[int] = mapped_column(Integer, Identity(start=1, cycle=True), primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Relationships
    majors: Mapped[List["StudentMajor"]] = relationship(
        "StudentMajor", back_populates="student", cascade="all, save-update, delete-orphan"
    )
    sections: Mapped[List["Enrollment"]] = relationship(
        "Enrollment", back_populates="student", cascade="all, save-update, delete-orphan"
    )
    
    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database. In this case, we want two separate uniqueness constraints (candidate keys).
    __table_args__ = (
        UniqueConstraint("first_name", "last_name", name="students_uk_01"),
        UniqueConstraint("email", name="students_uk_02")
    )

    def __init__(self, last_name: str, first_name: str, email: str):
        self.last_name = last_name
        self.first_name = first_name
        self.email = email

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

    def add_section(self, section):
        """Add a section to a list of sections the student is enrolled in currently."""
        for next_section in self.sections:
            if next_section.section == section:
                return  # Student already enrolled in section
        student_enrollment = Enrollment(section, self)
        section.students.append(student_enrollment)
        self.sections.append(student_enrollment)

    def delete_section(self, section):
        """Delete a section from the list of sections the student is enrolled in."""
        for next_section in self.sections:
            if next_section.section == section:
                self.sections.remove(next_section)
                return

    def __str__(self):
        return f"Student ID: {self.student_id} name: {self.last_name}, {self.first_name} e-mail: {self.email}"
