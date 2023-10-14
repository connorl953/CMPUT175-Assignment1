#----------------------------------------------------
# Assignment 1: Mini Bear Tracks
# Purpose of program: To roughly emulate UAlberta's Bear Tracks system.
#
# Author: Connor Li
# Collaborators/references: None
#----------------------------------------------------

class Course:
    def __init__(self, name, time, capacity, teacher):
        self.name = name  # i.e. COMP 151
        self.time = time  # i.e. MWF 9:00
        self.capacity = int(capacity)  # i.e. 156
        self.teacher = teacher


class Student:
    def __init__(self, name, student_id, program):
        self.name = name
        self.student_id = student_id
        self.program = program
        self.enrolled_courses = []
        self.timetable = [["" for _ in range(5)] for _ in range(18)]


def create_bottom_cell(chunk_width):
    string_builder = []

    string_builder.append(" ".center(chunk_width) + "|\n")
    string_builder.append(" ".center(chunk_width) + "|\n")
    string_builder.append(("-" * chunk_width).center(chunk_width) + "|\n")

    return ''.join(string_builder)


def create_special_bottom_cell(chunk_width):
    # based on Java's StringBuilder object, makes code more human-readable

    string_builder = []

    string_builder.append(" ".center(chunk_width) + "|\n")
    string_builder.append(" ".center(chunk_width) + "|\n")
    string_builder.append(("-" * chunk_width).center(chunk_width) + "+\n")

    return ''.join(string_builder)


def create_empty_cell(chunk_width):
    string_builder = []

    string_builder.append(" ".center(chunk_width) + "|\n")
    string_builder.append(" ".center(chunk_width) + "|\n")
    string_builder.append(" ".center(chunk_width) + "|\n")

    return ''.join(string_builder)


def create_top_cell(class_name, class_location, chunk_width):
    string_builder = []

    if len(class_name.split(" ")[0]) > 4:
        class_name = class_name[0:3] + "* " + class_name.split(" ")[1]

    string_builder.append("" + class_name.center(chunk_width) + "|\n")
    string_builder.append(class_location.center(chunk_width) + "|\n")
    string_builder.append("".center(chunk_width) + "|\n|")
    return ''.join(string_builder)


def index_to_time(index_int):
    hour = int(index_int / 2)
    if index_int % 2 == 0:
        return str(hour) + ":00"
    else:
        return str(hour) + ":30"


class TableRenderer:
    def __init__(self, table, chunk_width):
        self.table = table
        self.pretty_table = self.create_pretty_table(chunk_width)

    def render_table(self):
        """
        Renders the timetable to the console,

        self.table is a 2D list of strings, 5 across and 18 down.
        Each string is a course name and location, or an empty string.

        """
        self.print_pretty_table()

    def create_pretty_table(self, chunk_width):
        """
        This method creates a 'pretty table' with specific formatting rules. The table is initially filled with empty strings.
        Then, for each block in the original table, it applies different formatting rules depending on the position of the block
        and the day of the week it represents (Monday, Wednesday, Friday or Tuesday, Thursday).

        The method uses helper functions to create different types of cells: top cells, bottom cells, special bottom cells,
        and empty cells. Each cell is created with a specified chunk width.

        This method was chosen over the line-by-line approach because it is more modular, readable, efficient, and flexible.
        Despite this, the table is still rendered line-by-line in the print_pretty_table() method.

        The pretty table is returned as a 2D list of strings.

        Parameters:
            chunk_width (int): The width of each cell in the pretty table.

        Returns:
            pretty_table (list): A 2D list of strings representing the pretty table.
        """
        pretty_table = [["" for _ in range(5)] for _ in range(18)]
        table = self.table
        for y in range(len(self.table)):  # foreach row in table, but with indexes.
            for x in range(len(table[y])):  # foreach block in row, but with indexes.
                block = table[y][x]
                # Grab the block from the student's timetable (this holds the data for the pretty table)

                # MWF blocks start at y = 0, 2, 4, etc
                if y % 2 == 0:
                    for i in range(0, 5, 2):
                        pretty_table[y + 1][i] = create_bottom_cell(chunk_width)

                # TR blocks start at y = 0, 3, 6, 9, etc
                if y % 3 == 0:
                    for i in range(1, 4, 2):
                        pretty_table[y + 2][i] = create_bottom_cell(chunk_width)

                # Full special lines attempted at y = 5 , 11, 17
                if (y + 1) % 6 == 0:
                    for i in range(5):
                        pretty_table[y][i] = create_special_bottom_cell(chunk_width)

                if block != "":  # if the block is not empty, then it must be a course
                    course_name = block.split(" ")[0]
                    course_number = block.split(" ")[1]
                    course_capacity = block.split(" ")[2]
                    if x % 2 == 0:  # if x is even, then it must be monday wednesday or friday
                        pretty_table[y][x] = create_top_cell(course_name + " " + course_number,
                                                             course_capacity, chunk_width)
                        pretty_table[y + 1][x] = create_bottom_cell(chunk_width)
                    elif x % 2 == 1:  # if not, then it must be tuesday or thursday
                        pretty_table[y][x] = create_top_cell(course_name + " " + course_number,
                                                             course_capacity, chunk_width)
                        pretty_table[y + 1][x] = create_empty_cell(chunk_width)
                        pretty_table[y + 2][x] = create_bottom_cell(chunk_width)
                    if y > 0:  # if not the first row, and is a course, then the previous row must be a bottom cell
                        pretty_table[y - 1][x] = create_bottom_cell(chunk_width)
                else:
                    if (pretty_table[y][x]) == "":  # final check to make sure the pretty cell is not truly empty
                        pretty_table[y][x] = create_empty_cell(chunk_width)

        return pretty_table

    def print_pretty_table(self):
        """
        This function is used with the create_pretty_table() function to render the timetable to the console.

        Renders the timetable to the console line-by-line using the pre-made pretty table.

        This function does not return anything.
        """
        print("".ljust(5) + "    Mon        Tues       Wed       Thurs       Fri    ")
        print("".ljust(5) + "+----------+----------+----------+----------+----------+")
        time_index = 16
        row = 0
        line = 0
        while line < len(self.pretty_table) * 3:
            # Treat the 2d array as a giant string, ignoring newlines,
            # and iterate through every line
            if line % 3 == 0:  # There are always 3 lines in every "cell",
                # print the time next to the start of every cell
                print(index_to_time(time_index).ljust(5), end="")
                time_index += 1
            else:
                print("".ljust(5), end="")

            if "+" in self.pretty_table[row][1].split("\n")[line - (row * 3)]:
                print("+", end="")
            else:
                print("|", end="")

            for string in self.pretty_table[row]:
                print(string.split("\n")[line - (row * 3)], end="")
            line += 1
            print()
            if line % 3 == 0:
                row += 1



def main():
    # Afternote: I chose to use student and course objects in their own lists because the object-oriented approach is
    # more scalable and easier to maintain than using a complicated web of lists and dictionaries. More importantly,
    # it avoids the complexity that could arise from managing interconnected lists and dictionaries.

    # Initialize list of students
    students = []
    # Initialize list of courses
    courses = []

    # These are not parallel lists; they are independent of each other.

    try:
        # Parse courses from courses.txt in following format: CMPUT 101; TR 14:00; 156; Marianne Morris,
        # with 156 being the room number
        with open("courses.txt", "r") as f:
            for line in f:
                if len(line) > 1:
                    line = line.strip()
                    line = line.split(";")
                    course = Course(line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip())
                    courses.append(course)

        # Parse students from students.txt in following format: 123456, SCI , Mary Lou Soleiman
        # Add enrolledCourses from enrollment.txt to student objects in the following format: CMPUT 175: 123456

        with open("students.txt", "r") as f:
            for line in f:
                if len(line) > 1:
                    line = line.strip()
                    line = line.split(",")
                    student = Student(line[2].strip(), line[0].strip(), line[1].strip())
                    with open("enrollment.txt", "r") as f2:
                        for line2 in f2:
                            if len(line2) > 1:
                                line2 = line2.strip()
                                line2 = line2.split(":")
                                student_id = line2[1].strip()
                                course_name = line2[0].strip()
                                if student_id == student.student_id:
                                    for course in courses:
                                        if course_name == course.name:
                                            student.enrolled_courses.append(course)
                                            course.capacity -= 1

                student.timetable = generate_timetable(student)
                students.append(student)
    except FileNotFoundError:
        print("Error: File does not exist")
    except IndexError:
        raise Exception("File is not formatted correctly. (Are you missing a seperator?)")

    try:
        while True:
            print("==========================")
            print("Welcome to Mini-BearTracks")
            print("==========================")
            print("What would you like to do?")
            print("1. Print timetable")
            print("2. Enroll in course")
            print("3. Drop course")
            print("4. Quit")

            choice = prompt()

            # Dictionary where the key is the choice and the value is the function to call, emulates Java switch
            # notation
            choices = {
                1: print_timetable,
                2: enroll_in_course,
                3: drop_course,
                4: quit,
            }
            func = choices.get(choice)
            if choice == 2 or choice == 3:
                func(students, courses)
            elif choice == 4:
                save_data(students, courses)
                func("Goodbye")
            else:
                func(students)
    except KeyboardInterrupt:
        save_data(students, courses)
        print("Goodbye")


def print_timetable(students):
    """
    Prints the timetable for a given student.

    The function first gets the student ID from the list of students. If the student ID is invalid, it prints an error message and returns.
    Otherwise, it retrieves the student details using the student ID and prints the student's timetable.

    Args:
        students (list): The list of students.

    Returns:
        None
    """
    student_id = get_student_id_input(students)

    if student_id == "-1":
        print("Invalid student ID. Cannot print timetable.")
        return

    student = get_student_by_id(student_id, students)
    print("Timetable for " + student.name + ", in the faculty of " + student.program + ":")

    table_renderer = TableRenderer(student.timetable, 10)
    table_renderer.render_table()


def get_student_by_id(id, students):
    for student in students:
        if student.student_id == id:
            return student


def get_student_id_input(student_list):
    student_id = input("Student ID: ").strip()
    for student in student_list:
        if student.student_id == student_id:
            return student_id
    return "-1"


def enroll_in_course(students, courses):
    student_id = get_student_id_input(students)

    if student_id == "-1":
        print("Invalid student ID. Cannot continue with course enrollment.")
        return

    student = get_student_by_id(student_id, students)
    course_name = input("Course name: ").strip().upper()

    status = check_course_enrollable(student, course_name, courses)
    if status == "OK":
        for course in courses:
            if course.name.upper() == course_name:
                student.enrolled_courses.append(course)
                course.capacity -= 1
                student.timetable = generate_timetable(student)
                print(student.name + " has successfully been enrolled in " + course.name + ", on " + course.time + ".")
                return
    else:
        print(status)


def check_course_enrollable(student, course_name, course_list):
    """
    Checks if a student is eligible to enroll in a given course.

    This function checks if the course exists, if the student is already enrolled in the course, if the course is at capacity,
    and if the course time conflicts with the times of other courses the student is enrolled in.

    Args:
        student (Student): The student attempting to enroll in the course.
        course_name (str): The name of the course the student is attempting to enroll in.
        course_list (list): The list of all available courses.

    Returns:
        str: A message indicating whether the student can enroll in the course or the reason why they cannot.
    """
    selected_course = None

    for course in course_list:
        if course.name.upper() == course_name:
            selected_course = course

    if selected_course is None:
        return "Course \"" + course_name + "\" does not exist"

    if selected_course in student.enrolled_courses:
        return "Schedule conflict: already registered for course on " + selected_course.time.split(" ")[0]

    if selected_course.capacity < 1:
        return "Cannot enroll." + course_name + " is already at capacity. Please contact advisor to get on waiting list."

    for course in student.enrolled_courses:
        days = course.time.split(" ")[0]
        time_index = time_to_index(course.time.split(" ")[1])
        selected_course_days = selected_course.time.split(" ")[0]
        selected_course_time_index = time_to_index(selected_course.time.split(" ")[1])
        if days == selected_course_days:
            if days == "MWF":
                if abs(time_index - selected_course_time_index) < 2:
                    return "Selected course conflicts with course \"" + course.name + "\" on " + course.time
            elif days == "TR":
                if abs(time_index - selected_course_time_index) < 3:
                    return "Selected course conflicts with course \"" + course.name + "\" on " + course.time

    return "OK"


def drop_course(students, courses):
    """
    Drops a course for a student.

    This function first gets the student ID from the user. If the ID is invalid, it prints an error message and returns.
    Then, it prompts the user to select a course to drop from the student's enrolled courses.
    If the selected course can be dropped, it removes the course from the student's enrolled courses, increases the course's capacity by 1,
    regenerates the student's timetable, and prints a success message. If the course cannot be dropped, it prints an error message.

    Args:
        students (list): The list of students.
        courses (list): The list of courses.

    Returns:
        None
    """
    student_id = get_student_id_input(students)
    if student_id == "-1":
        print("Invalid student ID. Cannot continue with course drop.")
        return

    print("Select course to drop:")
    student = get_student_by_id(student_id, students)
    for course in student.enrolled_courses:
        print(course.name)

    selected_course = input("> ").strip().upper()
    droppable_status = check_course_droppable(student, selected_course, courses)
    if droppable_status == "OK":
        for course in student.enrolled_courses:
            if course.name.upper() == selected_course:
                student.enrolled_courses.remove(course)
                course.capacity += 1
                student.timetable = generate_timetable(student)
                print(student.name + " has successfully dropped " + course.name + ".")
    else:
        print(droppable_status)


def check_course_droppable(student, course_name, course_list):
    """
    Checks if a student can drop a course from their enrolled courses.

    This function first checks if the course exists in the course list. If the course does not exist, it returns a message indicating that the student is not registered in the course.

    Then, it checks if the student is enrolled in the course. If the student is not enrolled in the course, it returns a message indicating that the student is not enrolled in the course.

    If the student is enrolled in the course and the course exists, it returns "OK".

    Args:
        student (object): The student object.
        course_name (str): The name of the course to be dropped.
        course_list (list): The list of all courses.

    Returns:
        str: A message indicating whether the student can drop the course or not.
    """
    selected_course = None

    for course in course_list:
        if course.name.upper() == course_name:
            selected_course = course

    if selected_course is None:
        return "Drop failed. " + student.name + " is not currently registered in " + course_name + "."

    if selected_course not in student.enrolled_courses:
        return "Student \"" + student.name + "\" is not enrolled in course \"" + course_name + "\""

    return "OK"


def save_data(students, courses):
    """
    Saves student, course, and enrollment data to respective text files.

    This function saves the enrollment data to 'enrollment.txt', course data to 'courses.txt', and student data to 'students.txt'.
    The function also adjusts the course capacities to reflect the number of enrolled students.

    Args:
        students (list): A list of Student objects.
        courses (list): A list of Course objects.

    Files Accessed:
        enrollment.txt: Contains enrollment data in the format 'Course Name: Student ID'.
        courses.txt: Contains course data in the format 'Course Name; Course Time; Course Capacity; Course Teacher'.
        students.txt: Contains student data in the format 'Student ID, Student Program, Student Name'.
    """

    # Save enrollment data to enrollment.txt, example line: CMPUT 175: 123456
    # Save course data to courses.txt, example line: CMPUT 101; TR 14:00; 156; Marianne Morris
    # Save student data to students.txt, example line: 123456, SCI , Mary Lou Soleiman

    # Save enrollment data
    with open("enrollment.txt", "w") as f:
        for student in students:
            for course in student.enrolled_courses:
                f.write(course.name + ": " + student.student_id + "\n")

    for student in students:  # Reset course capacities
        for course in student.enrolled_courses:
            course.capacity += 1

    # Save course data
    with open("courses.txt", "w") as f:
        for course in courses:
            f.write(course.name + "; " + course.time + "; " + str(course.capacity) + "; " + str(course.teacher) + "\n")

    for student in students:  # Re-enroll students after saving true course capacities
        for course in student.enrolled_courses:
            course.capacity -= 1

    # Save student data
    with open("students.txt", "w") as f:
        for student in students:
            f.write(student.student_id + ", " + student.program + ", " + student.name + "\n")


def generate_timetable(student):
    """
     This function generates a timetable for a given student.

     Parameters:
     student (Student): The student for whom the timetable is being generated.

     The function works as follows:
     1. Create a 2D array (timetable) with rows representing half-hour time slots and columns representing weekdays.
     2. For each course in the student's enrolledCourses list:
        a. Get the course name, days, time, and location.
        b. Convert the time to an index in the timetable array.
        c. If the course is on MWF, add the course name and location to the timetable at the appropriate indices.
        d. If the course is on TR, add the course name and location to the timetable at the appropriate indices.
        e. If the course is on a weekend, do nothing.
        f. Repeat step b for each course in the student's enrolledCourses list.
     4. Return the timetable.

     :returns: A 2D array representing the student's timetable.
     """

    timetable = [["" for _ in range(5)] for _ in range(18)]
    for course in student.enrolled_courses:
        course_name = course.name
        course_days = course.time.split(" ")[0]  # string like MWF
        course_time = course.time.split(" ")[1]  # string like 14:00
        course_capacity = str(course.capacity)
        time_index = time_to_index(course_time)

        if course_days == "MWF":
            timetable[time_index][0] = course_name + " " + course_capacity
            timetable[time_index][2] = course_name + " " + course_capacity
            timetable[time_index][4] = course_name + " " + course_capacity
        elif course_days == "TR":
            timetable[time_index][1] = course_name + " " + course_capacity
            timetable[time_index][3] = course_name + " " + course_capacity



    return timetable


def time_to_index(time_str):
    """
    Converts a time string in the format 'HH:MM' to an index.

    The function assumes that the time starts at 08:00 and increments in 30 minute intervals. For example, 08:00 corresponds to an index of 0, 08:30 corresponds to an index of 1, 09:00 corresponds to an index of 2, and so on.

    Args:
        time_str (str): The time string to convert, in the format 'HH:MM'.

    Returns:
        int: The index corresponding to the given time string.
    """
    hour = int(time_str.split(":")[0])
    minute = int(time_str.split(":")[1])
    index = (hour - 8) * 2
    if minute == 30:
        index += 1

    return index


def prompt():
    while True:
        try:
            choice = int(input("> "))
            if choice < 1 or choice > 4:
                raise ValueError

            return choice
        except ValueError:
            print("Sorry, invalid entry. Please enter a choice from 1 to 4.")


main()
