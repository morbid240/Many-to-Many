from Section import Section
from Department import Department
from Course import Course
from Student import Student
from Major import Major
from QuerySelect import select_course, select_department, select_major, select_section, select_student
from db_connection import Session


def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def delete_course(session: Session):
    """
    Prompt the user to select a course by department abbreviation and course number, then delete it.
    :param session: The connection to the database.
    :return: None
    """
    print("Deleting a course")
    course = select_course(session)
    if 0 < session.query(Sections).filter(Section.courseNumber == course.courseNumber).count():
        print("Sections depend on this course, go delete them first and try again.")
    else:
        session.delete(course)


def delete_section(session: Session):
    """
    Prompt the user to select a section by its attributes, then delete it.
    :param session: The connection to the database.
    :return: None
    """
    print("Deleting a section")
    section = select_section(session)
    session.delete(section)


def delete_student(session: Session):
    """
    Prompt the user for a student to delete and delete them.
    :param session:     The current connection to the database.
    :return:            None
    """
    student: Student = select_student(session)
    """This is a bit ghetto.  The relationship from Student to StudentMajor has 
    cascade delete, so this delete will work even if a student has declared one
    or more majors.  I could write a method on Student that would return some
    indication of whether it has any children, and use that to let the user know
    that they cannot delete this particular student.  But I'm too lazy at this
    point.
    """
    session.delete(student)


def delete_major_student(sess: Session):
    """Remove a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the major and the student who no longer has that major.")
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    major.remove_student(student)


def delete_student_major(sess: Session):
    """Undeclare a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student.remove_major(major)


def delete_student_section(sess: Session):
    """Unenroll student from a section"""
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    section: Major = select_section(sess)
    student.delete_section(section)

