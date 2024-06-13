from Section import Section
from QueryCourse import select_course
from db_connection import Session

def add_section(session: Session):
    """
    Prompt the user for the information for a new section and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which course are you adding this section?")
    course = select_course(session)
    section_number = int(input("Enter the Section Number --> "))
    section_year = int(input("Enter the Section Year --> "))
    semester = input("Enter the Semester --> ")
    schedule = input("Enter Schedule --> ")
    start_time = Time(input("Enter Start Time (HH:MM:SS) --> "))
    violation = True  # Flag that we still have to prompt for fresh values
    while violation:
        building = input("Section Building --> ")
        room = int(input("Section Room --> "))
        instructor = input("Instructor --> ")
        section = Section(course, section_number, section_year, semester, schedule, start_time, building, room, instructor)
        violated_constraints = check_unique(Session, course)

        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(section)


def delete_section(session: Session):
    """
    Prompt the user to select a section by its attributes, then delete it.
    :param session: The connection to the database.
    :return: None
    """
    print("Deleting a section")
    section = select_section(session)
    session.delete(section)
    

def select_section(session: Session):
    """
    Select a section by its attributes.
    :param sess: The connection to the database.
    :return: The selected section.
    """
    found = False
    while not found:
        department_abbreviation = input("Department Abbreviation --> ")
        course_number = int(input("Course Number --> "))
        section_number = int(input("Section Number --> "))
        semester = input("Semester --> ")
        section_year = int(input("Section Year --> "))

        count = sess.query(Section).filter(Section.departmentAbbreviation == department_abbreviation,
                   Section.courseNumber == course_number,
                   Section.sectionNumber == section_number,
                   Section.semester == semester,
                   Section.sectionYear == section_year).count()
        found = count == 1
        if not found:
          print("No section found with that information. Please try again.")
    # Otherwise its been found
    return sess.query(Section).filter(Section.departmentAbbreviation == department_abbreviation,
            Section.courseNumber == course_number, Section.sectionNumber == section_number,
           Section.semester == semester, Section.sectionYear == section_year).first()
