from sqlalchemy import Column, Integer, String, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm_base import Base

class Enrollment(Base):
    """Association class between students and sections."""
    __tablename__ = "enrollments"
    
    # Composite primary key
    studentID: Mapped[int] = mapped_column('student_id', Integer, primary_key=True)
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10), primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', Integer, primary_key=True)
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer, primary_key=True)
    
    # Relationships
    section: Mapped["Section"] = relationship("Section", back_populates="students")  
    student: Mapped["Student"] = relationship("Student", back_populates="sections") 
    
    # Constraints
    __table_args__ = (
        # Foreign key constraint to ensure the section exists
        ForeignKeyConstraint(
            ['departmentAbbreviation', 'courseNumber', 'sectionNumber', 'semester', 'sectionYear'],
            ['sections.department_abbreviation', 'sections.course_number', 'sections.section_number', 'sections.semester', 'sections.section_year']
        ),
        # Foreign key constraint to ensure the student exists
        ForeignKeyConstraint(
            ['studentID'],
            ['students.student_id']
        ),
        # Unique constraint to ensure a student cannot enroll in the same course more than once per semester
        UniqueConstraint('studentID', 'departmentAbbreviation', 'courseNumber', 'semester', name='uq_student_course_semester')
    )
    
    def __init__(self, section, student):
        self.set_section(section)
        self.set_student(student)

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