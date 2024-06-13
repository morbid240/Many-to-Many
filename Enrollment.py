from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKeyConstraint
from typing import List 


from Student import Student 
from Section import Section
'''
a.	Uniqueness Constraints

    i.	This will have, as an OO attribute, a reference to Student and Section.

    ii.	Obviously, as Enrollment is the association class between Student and Section, 
        the primary key of Enrollment must be the combination of the primary key migrating 
        into Enrollment from Student and the primary key migrating into Enrollment from Section.

    iii.	
        We want to be sure that no student enrolls in the same course more than once in the same semester.  
        For instance, you would not want a student to be able to enroll in section 01 of CECS 323 for Fall 
        of 2023 and section 03 of CECS 323 for Fall of 2023.  One way is to create a 
        uniqueness constraint {department_abbreviation, course_number, section_year, semester, student_id}. 
        But that only works if those columns migrate into enrollments from sections.  If you gave sections a surrogate, 
        you will have to find some other way to enforce this constraint.

b.	Student will have a List of instances of Enrollment that it manages so that the Student instance “knows” 
    all Sections that they are enrolled in.
c.	Section will also have a List of instances of Enrollment so that Section “knows” who all the students 
    are who are enrolled in that Section.
d.	In the sample code, youll see a method on Student called add_major that populates the StudentMajor class 
    when a student declares a new Major.  A similar function: add_student appears in Major.  
    You will need to do the same for Student and Section to allow for each of those to maintain the Many to Many between them.
e.	Be careful that the primary key of Enrollment is 
        {student_id, department_abbreviation, course_number, section_number, section_year, semester}. 
         I will understand if you decide at this point to add a surrogate to Section.

'''

class Enrollment(Base):
    __tablename__ = "enrollments"  # Give SQLAlchemy th name of the table.
    # Primary keys 

    # Define relationships 
    student: Mapped["Student"] = relationship(back_populates="enrollments")  # 0 student many enrollments
    sections: Mapped[List["Section"]] = relationship(back_populates="enrollment") # many sections zero enrollments

    __table_args__ = (
        ForeignKeyConstraint([departmentAbbreviation, courseNumber, sectionYear, semester, student_id], 
                             [Section.departmentAbbreviation, Section.courseNumber, Section.semester, Student.student_id])
    )

    def __init__(self, section: Section, student: Student ):
        self.set_section(section)
        self.set_student(section)

            
    ## TODO add setters for student and section, fix str
    def __str__(self):
        return f"Student ID: {self.studentID} name: {self.lastName}, {self.firstName} e-mail: {self.email}"
