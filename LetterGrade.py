
"""
Malcolm Roddy
Inheritance HW
Due Date: 06/23/2024


"""


from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, String, UniqueConstraint, CheckConstraint

from Enrollment import Enrollment



class LetterGrade(Enrollment):

    """
    Subclass of Enrollment representing letter grades.
    """
        
    __tablename__ = "letter_grade"
    
    grade: Mapped[int] = mapped_column(
        'grade_id', ForeignKey(
                "enrollments.enrollment_id", ondelete="CASCADE"
        ), 
        primary_key=True
    )

    minSatisfactory: Mapped[str] = mapped_column("min_satisfactory", String(1), nullable=False)


    # Constraints
    __table_args__ = (
        CheckConstraint(minSatisfactory.in_(['A', 'B', 'C', 'D', 'F']), name='letter_grade_uk_01'),
    )

    __mapper_args__ = {
        "polymorphic_identity": "letter_grade"
    }

    __table_args__ = (
        CheckConstraint(minSatisfactory.in_(['A', 'B', 'C', 'D', 'F']), name='check_min_satisfactory'),
    )

    def __init__(self, section, student, min_satisfactory: str, grade: str):
        super().__init__(section, student)
        self.minSatisfactory = min_satisfactory
        self.grade = grade


    def __str__(self):
        return f"LetterGrade - student: {self.student}, section: {self.section}, grade: {self.grade}, minSatisfactory: {self.minSatisfactory}"

