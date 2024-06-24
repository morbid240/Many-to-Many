
"""
Malcolm Roddy
Inheritance HW
Due Date: 06/23/2024


"""


from sqlalchemy import Date, ForeignKey, String, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from Enrollment import Enrollment



class LetterGrade(Enrollment):

    """
    Subclass of Enrollment representing letter grades.
    """
        
    __tablename__ = "letter_grades"
    
    # Defining our pk and inheritance 
    gradeId: Mapped[int] = mapped_column(
        'grade_id', # name of pk in table
        # ensure we got cascade delete on and set it as a pk 
        ForeignKey("enrollments.enrollment_id", ondelete="CASCADE"), 
        primary_key=True
    )

    # Another attribute 
    minSatisfactory: Mapped[str] = mapped_column("min_satisfactory", String(1), nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint(min_satisfactory.in_(['A', 'B', 'C', 'D', 'F']), name='letter_grade_uk_01'),
    )


    # Constructor
    def __init__(self, section, student, min_satisfactory: str, grade: str):
        super().__init__(section, student)
        self.minSatisfactory = min_satisfactory
        self.grade = grade


    def __str__(self):
        return f"LetterGrade - student: {self.student}, section: {self.section}, grade: {self.grade}, minSatisfactory: {self.minSatisfactory}"

