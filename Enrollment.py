"""
Malcolm Roddy 
CECS 323
Many to Many
Due Date: 06/14/2024

This contains the association class that connects Students
with Sections. 
Basically a rip off from StudentMajor 
Essentially contains only foreign keys from Student/Sections

Todo: store data time instance 
"""

from sqlalchemy import Column, Integer, String, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm_base import Base
from datetime import datetime


class Enrollment(Base):
    __tablename__ = "enrollments"
    
    # Composite primary key
    student_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_abbreviation: Mapped[str] = mapped_column(String(10), primary_key=True)
    course_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    semester: Mapped[str] = mapped_column(String(10), primary_key=True)
    section_year: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Relationships
    section: Mapped["Section"] = relationship("Section", back_populates="students")  
    student: Mapped["Student"] = relationship("Student", back_populates="sections") 
    
    # Constraints
    __table_args__ = (
        # Foreign key constraint to ensure the section exists
        ForeignKeyConstraint(
            ['department_abbreviation', 'course_number', 'section_number', 'semester', 'section_year'],
            ['sections.department_abbreviation', 'sections.course_number', 'sections.section_number', 'sections.semester', 'sections.section_year']
        ),
        # Foreign key constraint to ensure the student exists
        ForeignKeyConstraint(
            ['student_id'],
            ['students.student_id']
        ),
        # Unique constraint to ensure a student cannot enroll in the same course more than once per semester
        UniqueConstraint('student_id', 'department_abbreviation', 'course_number', 'semester', name='uq_student_course_semester')
    )
    
    
    """Set methods to create student/section without constraints since it depends on them 
    just like how Course needed a set_department to setup column mapping for FK
    Since this class has only FK attributes, I assume we only take section and student as arguments to 
    fill out columns
    """
    def __init__(self, section, student):
        self.set_section(section)
        self.set_student(student)

    def set_student(self, student):
        self.student = student
        self.student_id = student.student_id

    def set_section(self, section):
        self.section = section
        self.department_abbreviation = section.department_abbreviation
        self.course_number = section.course_number
        self.section_number = section.section_number
        self.semester = section.semester
        self.section_year = section.section_year
