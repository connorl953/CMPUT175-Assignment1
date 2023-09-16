class Student:
    def __init__(self, name, studentID, program):
        self.name = name
        self.studentID = studentID
        self.program = program
        self.enrolledCourses = []
        self.timetable = [["" for _ in range(5)] for _ in range(18)]