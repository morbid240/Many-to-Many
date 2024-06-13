from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List                 # Use this for the list of courses offered by the department


class Department(Base):
    __tablename__ = "departments"  # Give SQLAlchemy th name of the table.
    # Primary key
    abbreviation: Mapped[str] = mapped_column('abbreviation', String, nullable=False, primary_key=True)
    
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    # Relationships
    majors: Mapped[List["Major"]] = relationship(back_populates="department")
    courses: Mapped[List["Course"]] = relationship(back_populates="department")
    # Unniqueness constraints 
    __table_args__ = (UniqueConstraint("name", name="departments_uk_01"), )

    # "Constructor"
    def __init__(self, abbreviation: str, name: str):
        self.abbreviation = abbreviation
        self.name = name

    def add_course(self, course):
        if course not in self.courses:
            self.courses.add(course)            # I believe this will update the course as well.

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return f"Department: {self.abbreviation}: {self.name} \n\tnumber course offered: {len(self.courses)}\n"
