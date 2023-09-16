from Student import Student
from Course import Course
from TableRenderer import TableRenderer


def main():
    # Initialize list of students
    students = []
    # Initialize list of courses
    courses = []
    try:
        # Parse courses from courses.txt in following format: CMPUT 101; TR 14:00; 156; Marianne Morris, with 156 being the room number
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
                print("student added: " + student.name + " " + student.studentID + " " + student.program)
                with open("enrollment.txt", "r") as f2:
                    for line2 in f2:
                        line2 = line2.strip()
                        line2 = line2.split(":")
                        student_id = line2[1].strip()
                        course_name = line2[0].strip()
                        if (student_id == student.studentID):
                            for course in courses:
                                if (course_name == course.name):
                                    student.enrolledCourses.append(course)
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
    func(students, courses)


def print_timetable(students, courses):
    student_id = input("Enter student ID: ").strip()
    for student in students:
        if (student.studentID == student_id):
            print("Printing timetable for " + student.name + "...")

            table_renderer = TableRenderer(student.timetable, 10, 3)
            table_renderer.render_table()
            #
            # print("         Mon        Tues       Wed       Thurs       Fri "+ "\n" +
            #       "+----------+----------+----------+----------+----------+")
            # hour = 16
            # for row in student.timetable:
            #     print(index_to_time(hour) + " ", end="")
            #     hour+=1
            #     for item in row:
            #         if (item == ""):
            #             print("Blank", end=" ")
            #         print(item, end="")
            #     print("\n")




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

    print("Generating timetable...")
    timetable = [["" for _ in range(5)] for _ in range(18)]
    for course in student.enrolledCourses:
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
    if (minute == 30):
        index += 1

    return index

def index_to_time(index_int):
    hour = int(index_int/2)
    if(index_int % 2 == 0):
        return str(hour) + ":00"
    else:
        return str(hour) + ":30"

def enroll_in_course():
    print("Enrolling in course...")


def drop_course():
    print("Dropping course...")


def quit():
    print("Quitting...")


def prompt():
    try:
        choice = int(input("> "))
        if (choice < 1 or choice > 4):
            raise ValueError
        print("Choice: " + str(choice))
        return choice
    except ValueError:
        print("Sorry, invalid entry. Please enter a choice from 1 to 4.")
        prompt()


main()
