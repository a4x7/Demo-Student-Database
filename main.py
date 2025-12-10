from datetime import datetime
def logger(action):
    def decorator(func):
        def wrapper(*args, **kwargs):
            f = open("log.txt", "a+")
            line = f"[{datetime.now()}] {action}: ({args[1]})\n"
            f.write(line)
            return func(*args, **kwargs)
        return wrapper
    return decorator
class Student:
    def __init__(self, name, roll, marks):
        if type(name) == str and name.isalpha():
            self.__name = name
        else:
            raise ValueError("Invalid name!")
        if len(roll) < 5:
            raise ValueError("Roll number is a 5 digit number!")
        try:
            self.__roll = int(roll)
        except:
            raise ValueError("Roll number must be an integer!")
        if type(eval(marks)) != list:
            raise TypeError("Marks must be in the form of a list!")
        marks = eval(marks)
        if len(marks) != 4:
            raise ValueError("4 marks must be provided!")
        for mark in marks:
            if not (mark >= 0 and mark <= 100):
                raise ValueError("Marks must be between 0 and 100!")
        self.__marks = marks
    def name(self):
        return self.__name
    def rollno(self):
        return self.__roll
    def marks(self):
        return self.__marks
    @property
    def average(self):
        return round(sum(self.__marks)/len(self.__marks), 2)
    def __str__(self):
        return f"Name: {self.__name}, Roll Number: {self.__roll}, Marks: {self.__marks}, Average: {self.average}"
    def __repr__(self):
        return f"(Name: {self.__name}, Roll Number: {self.__roll}, Marks: {self.__marks}, Average: {self.average})"
class StudentDB:
    def __init__(self, *args):
        self.__L = []
        try:
            for arg in args:
                if isinstance(arg, Student):
                    self.__L.append(arg)
                else:
                    raise TypeError("Student not found!")
        except TypeError as e:
            print(e)
    @logger("ADDED")
    def add_student(self, obj):
        try:
            if isinstance(obj, Student):
                for student in self.__L:
                    if student.rollno() == obj.rollno():
                        raise RollNoExists(obj.rollno())
                self.__L.append(obj)
            else:
                raise TypeError("Student not found!")
        except TypeError as e:
            return e
        except RollNoExists as e:
            return e
    @logger("REMOVED")
    def remove_student(self, roll):
        try:
            if type(roll) == int:
                self.__L.remove(self.find_student(roll))
            else:
                raise ValueError("Roll number must be a number!")
        except ValueError as e:
            print(e)
    def find_student(self, roll):
        try:
            for student in self.__L:
                if student.rollno() == int(roll):
                    return student
            raise StudentNotFound(roll)
        except ValueError:
            return "Roll number must be a number!"
        except StudentNotFound as e:
            return e
    @logger("SAVED")
    def save(self, filename):
        try:
            f = open(f"{filename}.txt", "w")
            names = []
            for i in self.__L:
                names.append(str(f"{i.name()}-{i.rollno()}-{i.marks()}-{i.average()}\n"))
            f.writelines(names)
            f.close()
        except FileNotFoundError:
            print("File does not exist!")
    @logger("LOADED")
    def load(self, filename):
        try:
            f = open(f"{filename}.txt")
            read = f.readlines()
            for i in read:
                r = i.split("-")
                name = r[0]
                rollno = r[1]
                marks = r[2]
                s = Student(name, rollno, marks)
                self.add_student(s)
            f.close()
        except FileNotFoundError:
            print("File does not exist!")
        except TypeError:
            print("Invalid file name!")
    def view(self):
        for i in self.__L:
            print(i)
    def count(self):
        return len(self.__L)
class StudentNotFound(Exception):
    def __init__(self, rollno):
        super().__init__(f"Roll number {rollno} not found!")
class RollNoExists(Exception):
    def __init__(self, rollno):
        super().__init__(f"Roll number {rollno} already exists!")
def main():
    print("\n", f"{'WELCOME TO THE DEMO STUDENT DATABASE':=^100}")
    db1 = StudentDB()
    while True:
        print("1.  Add\n2.  Remove\n3.  Search\n4.  Save\n5.  Load\n6.  View\n7.  Exit")
        inp = input().lower()
        if inp == "add" or inp == "1":
            std = Student(input("Enter name (alphabets only): "), input("Enter roll number (5 digits): "), input("Enter marks (list of 4): "))
            db1.add_student(std)
        elif inp == "remove" or inp == "2":
            roll = int(input("Enter roll number: "))
            db1.remove_student(roll)
        elif inp == "search" or inp == "3":
            roll = input("Enter roll number: ")
            print(db1.find_student(roll))
        elif inp == "save" or inp == "4":
            db1.save(input("Enter file name: "))
        elif inp == "load" or inp == "5":
            db1.load(input("Enter file name: "))
        elif inp == "view" or inp == "6":
            db1.view()
        elif inp == "exit" or inp == "7":
            print("GOODBYE!")
            break
if __name__ == "__main__":
    main()
