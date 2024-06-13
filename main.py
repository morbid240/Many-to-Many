import logging
from constants import *
from menu_definitions import menu_main, add_menu, delete_menu, list_menu, debug_select, introspection_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Major import Major
from Student import Student
from StudentMajor import StudentMajor
from Option import Option
from Menu import Menu
from pprint import pprint

"""
     Got tired of scrolling up and down for functions, 
     figured out a way for encapuslation. Im still a bit 
     confused agout scope here, but it seems like the session
     object is shared amongst all the functions the same way, 
     with them also being accessible here. 
    
    tried making a database manager module but had problems with scope  
"""

from QueryAdd import add_department, add_course, add_major, add_section, add_major_student, add_student, add_student_major, boilerplate
from QuerySelect import select_course, select_department, select_major, select_section, select_student, select_student_from_list
from QueryDelete import delete_course, delete_department, delete_major_student, delete_section, delete_student, delete_student_major
from QueryList import list_course, list_department, list_department_courses, list_major, list_major_student, list_student, list_student_major
# New functions made imported here
from QueryList import list_student_enrollment, list_enrolled_student
from QueryAdd import add_student_section, add_section_student
from QueryDelete import delete_student_section, delete_section_student

def add(sess: Session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(sess: Session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(sess: Session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)

    

if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    # Prompt the user for whether they want to introspect the tables or create all over again.
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print("starting over")
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our "Entity" classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
