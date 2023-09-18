# Author: Connor Li


class Course:
    def __init__(self, name, time, location):
        self.name = name  # i.e. COMP 151
        self.time = time  # i.e. MWF 9:00
        self.location = location  # i.e. 156


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

    """
    Renders the timetable to the console,

    self.table is a 2D list of strings, 5 across and 18 down.
    Each string is a course name and location, or an empty string.

    """

    def render_table(self):
        self.print_pretty_table()
        pass

    def create_pretty_table(self, chunk_width):
        pretty_table = [["" for _ in range(5)] for _ in range(18)]
        table = self.table
        for y in range(len(self.table)):  # foreach row in table, but with indexes.
            for x in range(len(table[y])):  # foreach block in row, but with indexes.
                block = table[y][x]

                # MWF blocks start at y = 0, 2, 4, etc
                # TR blocks start at y=0,3,6,9, etc
                # Full lines attempted at y = 5 , 11, 17

                if y % 2 == 0:
                    for i in range(0, 5, 2):
                        pretty_table[y + 1][i] = create_bottom_cell(chunk_width)

                if y % 3 == 0:
                    for i in range(1, 4, 2):
                        pretty_table[y + 2][i] = create_bottom_cell(chunk_width)

                if (y + 1) % 6 == 0:
                    for i in range(5):
                        pretty_table[y][i] = create_special_bottom_cell(chunk_width)

                if block != "":
                    if x % 2 == 0:  # if x is even, then it must be monday wednesday or friday
                        pretty_table[y][x] = create_top_cell(block.split(" ")[0] + " " + block.split(" ")[1],
                                                             block.split(" ")[2], chunk_width)
                        pretty_table[y + 1][x] = create_bottom_cell(chunk_width)
                    elif x % 2 == 1:  # if not, then it must be tuesday or thursday
                        pretty_table[y][x] = create_top_cell(block.split(" ")[0] + " " + block.split(" ")[1],
                                                             block.split(" ")[2], chunk_width)
                        pretty_table[y + 1][x] = create_empty_cell(chunk_width)
                        pretty_table[y + 2][x] = create_bottom_cell(chunk_width)
                    if y > 0:
                        pretty_table[y - 1][x] = create_bottom_cell(chunk_width)
                else:
                    if (pretty_table[y][x]) == "":
                        pretty_table[y][x] = create_empty_cell(chunk_width)

            for i in range(5):
                pretty_table[-1][i] = create_special_bottom_cell(chunk_width)

        return pretty_table

    def print_pretty_table(self):

        # TODO: Add times and dates to table

        print("".ljust(5) + "    Mon        Tues       Wed       Thurs       Fri    ")
        print("".ljust(5) + "+----------+----------+----------+----------+----------+")
        time_index = 16
        row = 0
        line = 0
        while line < len(self.pretty_table) * 3:
            # Treat the 2d array as a giant string, ignoring newlines,
            # and iterate through every line
            if line % 3 == 0:  # There are always 3 newlines in every "cell", print the time next to the start of every cell
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
                last = string
            line += 1
            print()
            if line % 3 == 0:
                row += 1
        pass


def main():
    # Initialize list of students
    students = []
    # Initialize list of courses
    courses = []
    try:
        # Parse courses from courses.txt in following format: CMPUT 101; TR 14:00; 156; Marianne Morris,
        # with 156 being the room number
        with open("courses.txt", "r") as f:
            for line in f:
                line = line.strip()
                line = line.split(";")

                course = Course(line[0].strip(), line[1].strip(), line[2].strip())
                courses.append(course)
                for course in courses:
                    print("course added: " + course.name + " " + course.time + " " + course.location)

        # Parse students from students.txt in following format: 123456, SCI , Mary Lou Soleiman
        # Add enrolledCourses from enrollment.txt to student objects in the following format: CMPUT 175: 123456

        with open("students.txt", "r") as f:
            for line in f:
                line = line.strip()
                line = line.split(",")
                student = Student(line[2].strip(), line[0].strip(), line[1].strip())
                print("student added: " + student.name + " " + student.student_id + " " + student.program)
                with open("enrollment.txt", "r") as f2:
                    for line2 in f2:
                        line2 = line2.strip()
                        line2 = line2.split(":")
                        student_id = line2[1].strip()
                        course_name = line2[0].strip()
                        if student_id == student.student_id:
                            for course in courses:
                                if course_name == course.name:
                                    student.enrolled_courses.append(course)
                                    print("student " + student.name + " enrolled in " + course.name)

                student.timetable = generate_timetable(student)
                students.append(student)

    except FileNotFoundError:
        print("Error: File does not exist")

    print("==========================")
    print("Welcome to Mini-BearTracks")
    print("==========================")
    print("What would you like to do?")
    print("1. Print timetable")
    print("2. Enroll in course")
    print("3. Drop course")
    print("4. Quit")
    choice = prompt()
    # Dictionary mapping, where the key is the choice and the value is the function to call

    choices = {
        '1': print_timetable,
        '2': enroll_in_course,
        '3': drop_course,
        '4': quit,
    }
    func = choices.get(str(choice))
    func(students)


def print_timetable(students):
    student_id = input("Enter student ID: ").strip()
    for student in students:
        if student.student_id == student_id:
            print("Printing timetable for " + student.name + "...")

            table_renderer = TableRenderer(student.timetable, 10)
            table_renderer.render_table()


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
     """

    timetable = [["" for _ in range(5)] for _ in range(18)]
    for course in student.enrolled_courses:
        course_name = course.name
        course_days = course.time.split(" ")[0]  # string like MWF
        course_time = course.time.split(" ")[1]  # string like 14:00
        course_location = course.location
        time_index = time_to_index(course_time)

        print("time index: " + str(time_index))
        print(course_name + " " + course_days + " " + str(course_time) + " " + course_location)

        if course_days == "MWF":
            timetable[time_index][0] = course_name + " " + course_location
            timetable[time_index][2] = course_name + " " + course_location
            timetable[time_index][4] = course_name + " " + course_location
        elif course_days == "TR":
            timetable[time_index][1] = course_name + " " + course_location
            timetable[time_index][3] = course_name + " " + course_location
        else:
            pass

    return timetable


def time_to_index(time_str):
    hour = int(time_str.split(":")[0])
    minute = int(time_str.split(":")[1])
    index = (hour - 8) * 2
    if minute == 30:
        index += 1

    return index


def enroll_in_course():
    print("Enrolling in course...")


def drop_course():
    print("Dropping course...")


def quit():
    print("Quitting...")


def prompt():
    while True:
        try:
            choice = int(input("> "))
            if choice < 1 or choice > 4:
                raise ValueError
            print("Choice: " + str(choice))
            return choice
        except ValueError:
            print("Sorry, invalid entry. Please enter a choice from 1 to 4.")


main()
