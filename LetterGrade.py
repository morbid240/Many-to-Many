
"""
Malcolm Roddy
Inheritance HW
Due Date: 06/23/2024


"""


from sqlalchemy import Date, ForeignKey, String, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped

from Enrollment import Enrollment



class LetterGrade(Enrollment):

    """
    Subclass of Enrollment representing letter grades.
    """
        
    __tablename__ = "letter_grade"
    
    # Defining our pk and inheritance 
    gradeId: Mapped[int] = mapped_column(
        'grade_id', # name of pk in table
        # ensure we got cascade delete on and set it as a pk 
        ForeignKey("enrollments.enrollment_id", ondelete="CASCADE"), 
        primary_key=True
    )

    # Another attribute 
    minSatisfactory: Mapped[str] = mapped_column("min_satisfactory", String(1), nullable=False)


    """Constraints added here. Since we only got one pk no need really for this I think"""
    __table_args__ = (
        CheckConstraint(minSatisfactory.in_(['A', 'B', 'C', 'D', 'F']), name='letter_grade_uk_01'),
    )

    """This is what makes it defined as inheritable"""
    __mapper_args__ = {
        "polymorphic_identity": "letter_grade"
    }

    # Constructor
    def __init__(self, section, student, min_satisfactory: str, grade: str):
        super().__init__(section, student)
        self.minSatisfactory = min_satisfactory
        self.grade = grade


    def __str__(self):
        return f"LetterGrade - student: {self.student}, section: {self.section}, grade: {self.grade}, minSatisfactory: {self.minSatisfactory}"

