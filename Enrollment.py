from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKeyConstraint


class Enrollment(Base):
    """
    Association class between students and sections.
    """
    __tablename__ = "enrollments"  # Give SQLAlchemy th name of the table.
    # Primary keys - all migrating foreign keys I guess...
    studentID: Mapped[int] = mapped_column('student_id', Integer, primary_key=True)
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10), primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', Integer, primary_key=True)
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer, nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True)

    # Define relationships. Both 'parents' contain the lists to keep track of each other
    section: Mapped["Section"] = relationship("Section", back_populates="students")  
    student: Mapped["Student"] = relationship("Student", back_populates="sections") 
    
    __table_args__ = (
        # unique constraint makes sure that no student enrolls in the same course more than once the same semester
        UniqueConstraint(
            'studentID', 'departmentAbbreviation)', 'courseNumber', 'sectionNumber', 'semester', 
            'sectionYear', name = "enrollment_uk_01"
        ),
        # All values in this class are literally from sections and students so this is the meat of it
        ForeignKeyConstraint(
            ['departmentAbbreviation', 'courseNumber', 'sectionYear', 'semester', 'studentID'], 
            ['sections.departmentAbbreviation', 'sections.courseNumber', 'sections.semester', 'students.studentID']
        )
    )

    # Constructor 
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

