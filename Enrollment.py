from sqlalchemy import Column, Integer, String, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm_base import Base
"""tha k fuck it didnt delete""" 
class Enrollment(Base):
    """Association class between students and sections."""
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