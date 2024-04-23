import os

class prompt:
    def enter_program():
        """
        Allows the user to choose what they want to do.
        """
        global entry_choice
        entry_choice = input("Input 'r' to take register, 'a' to add student to register, 'd' to delete student from register, 'f' to check student attendance percentages, or 'q' to quit: ").strip().lower()

    def add_student():
        """
        allows user to add a student to the register
        """
 
        student_added = input("Input the name of the student you'd like to add: ").strip().lower()
        data_methods.add_everywhere(student_added)


    def del_student():
        """
        allows user to delete a student from the register.
        """
        student_deleted = input("Input the name of the student you'd like to delete: ").strip().lower()
        data_methods.delete_everywhere(student_deleted)

    def take_attendance(number, line_read):
        """
        Function to take attendance for a specific student.
        
        Parameters:
            number (int): The number of the student in the attendance list.
            line_read (str): The name of the student.
        """
        global attendance_status
        attendance_status = input(f"{number}. {line_read}: ").strip().lower()

class calculation:
    def classes_attended(attendance_dict, student_name):
        """
        Updates the attendance record for each student based on the attendance status.

        Parameters:
            attendance_dict (dict): A dictionary containing student names as keys and their attendance count as values.
            student_name (str): The name of the student whose attendance record needs to be updated.
        """
        if attendance_status == "p":
            attendance_dict[student_name.strip()] += 1
        elif attendance_status == "a":
            attendance_dict[student_name.strip()] += 0
        else:
            print("invalid input, try again")
            prompt.take_attendance(count, student_name.strip())
            calculation.classes_attended(attendance_dict, student_name)

    def percentage_calc(percentage_dict, attendance_dict, student_name, total_classes):
        """
        Calculate the percentage attendance for each student and updates the percentage dictionary. 

        Parameters:
            percentage_dict (dict): The dictionary containing the percentage attendance value for each student.
            attendance_dict (dict): The dictionary containing the attendance count for each student.
            student_name (str): The name of the student for whom the percentage attendance is to be calculated.
            total_classes (int): The total number of classes taught.
        """
        percentage_dict[student_name.strip()] = round((attendance_dict[student_name.strip()]/total_classes)*100, 2)



class file_methods:
    def create_file(new_file = ''):
        """
        Create a new file with the given filename if it does not already exist.

        Parameters:
            new_file (str): The name of the file to be created.
        """

        with open(new_file, 'x', encoding='utf-8') as file:
            pass

    def read_update_files(file_name = ''):
        """
        Reads and updates files containing attendance data for students.

        Parameters:
            file_name (str): The name of the file to be read and updated. Defaults to an empty string.
        """

        global count
        count = 0
        total_classes = 0
        student_total_attended = {}
        attendance_percentage = {}
        
        with open('attended.txt', 'r+', encoding='utf-8') as attended_file, open('classes.txt', 'r+', encoding='utf-8') as classes_file, open('percentage.txt', 'r+', encoding='utf-8') as percentage_file, open('register.txt', 'r', encoding='utf-8') as register_file:
            student_total_attended = eval(attended_file.read())
            attendance_percentage = eval(percentage_file.read())
            total_classes = eval(classes_file.read())

            total_classes += 1
            print("mark 'p' if present, and 'a' if absent")

            while True:
                count += 1
                student_name = register_file.readline()
                if not student_name:
                    break
                prompt.take_attendance(count, student_name.strip())
                calculation.classes_attended(student_total_attended, student_name)
                calculation.percentage_calc(attendance_percentage, student_total_attended, student_name, total_classes)

            for file in [attended_file, classes_file, percentage_file]:
                file.seek(0)
                file.truncate(0)
            
            attended_file.write(str(student_total_attended))
            classes_file.write(str(total_classes))
            percentage_file.write(str(attendance_percentage))


    def append_file(file_name = 'register.txt', text = ""):
        """
        Appends the given text to the specified file.

        Args:
            file_name (str, optional): The name of the file to append the text to. Defaults to 'register.txt'.
            text (str, optional): The text to append to the file.
        """

        with open(file_name, 'a+', encoding='utf-8') as file:
            file.seek(0)
            data = file.read(100)
            if len(data) > 0 :
                file.write("\n")
            file.write(text)

    def del_from_file(file_name = 'register.txt', text = ""):
        """
        Delete a specified text from a file.

        Args:
            file_name (str): The name of the file to modify. Defaults to 'register.txt'.
            text (str): The text to delete from the file.
        """

        delete_status = False
        with open(file_name, 'r+', encoding = 'utf-8') as file:
            student_names = file.readlines()
            file.seek(0)
            file.truncate(0)
            for name in student_names:
                if student_names.index(name) == len(student_names) - 2 and name.strip('\n') != text and delete_status == False:
                    file.write(name.strip('\n'))
                elif name.strip('\n') != text:
                    file.write(name.strip(''))
                else:
                    delete_status = True

class data_methods:
    def create_dictionary(file_name = 'register.txt'):
        """
        Creates a dictionary from a file containing student names.
        
        file_name: The name of the file to read the student names from. Defaults to 'register.txt'.
        """

        keys = []
        with open(file_name, 'r', encoding='utf-8') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                keys.append(line.strip())

        keys = tuple(keys)
        student_details = dict.fromkeys(keys, 0)
        return student_details

    def del_from_dict(file_name = '', text = ''):
        """
        Deletes a key-value pair from a dictionary stored in a file.

        Parameters:
            file_name (str): The name of the file where the dictionary is stored.
            text (str): The key(student) to be deleted from the dictionary.
        """

        read_content = {}
        with open(file_name, 'r+', encoding = 'utf-8') as file:
            read_content = eval(file.read())
            del read_content[text]
            file.seek(0)
            file.truncate(0)
            file.write(str(read_content))

    def add_to_dict(file_name = '', text = ''):
        """
        This function adds a new key-value pair to a dictionary stored in a file.

        Parameters:
            file_name: The name of the file where the dictionary is stored
            text: The key(student) to be added to the dictionary
        """

        read_content = {}
        with open(file_name, 'r+', encoding = 'utf-8') as file:
            read_content = eval(file.read())
            read_content[text] = 0
            file.seek(0)
            file.truncate(0)
            file.write(str(read_content))

    def add_everywhere(student_to_add):
        """
        Adds a student to the register, attendance, and percentage files.

        Parameters:
            student_to_add (str): The name of the student to be added to the register.
        """

        students = []
        if student_to_add.replace(' ', '').isalpha():
            with open('register.txt', 'r', encoding='utf-8') as file:
                for student in file.readlines():
                    students.append(student.strip('\n'))

            if student_to_add in students:
                print(f"{student_to_add} is already in your register")
            else:
                file_methods.append_file(text = student_to_add)
                data_methods.add_to_dict('attended.txt', student_to_add)
                data_methods.add_to_dict('percentage.txt', student_to_add)
                print(f"{student_to_add} has been added to your register")
        else:
            print("The student name needs to be a string with only alphabets, try again")
            prompt.add_student()

    def delete_everywhere(student_to_delete):
        """
        Deletes a student from the register, attendance, and percentage files.

        Parameters:
            student_to_delete (str): The name of the student to be deleted.
        """

        students = []
        if student_to_delete.replace(' ', '').isalpha():
            with open('register.txt', 'r', encoding='utf-8') as file:
                for student in file.readlines():
                    students.append(student.strip('\n'))

            if student_to_delete in students:
                file_methods.del_from_file(text = student_to_delete)
                data_methods.del_from_dict('attended.txt', student_to_delete)
                data_methods.del_from_dict('percentage.txt', student_to_delete)
                print(f"{student_to_delete} has been removed from your register")
            else:
                print(f"{student_to_delete} is not in your register")
        else:
            print("The student name needs to be a string with only alphabets, try again")
            prompt.del_student()

    def display(file_name = 'percentage.txt'):
        """
        Display the percentage values stored in the percentage file.

        Parameters:
            file_name (str): The name of the file to read. Defaults to 'percentage.txt'.
        """

        with open(file_name, 'r', encoding='utf-8') as file:
            percentages = eval(file.read())
            for key, value in percentages.items():
                print(f"{key}:{value}%")

class actions:
    def code_runner():
        """
        Creates necessary files if they don't exist, then enters a while loop 
        to prompt for user input until the user chooses to quit. 
        The function handles various user inputs.
        """
        try:
            while True:
                prompt.enter_program()

                if entry_choice == 'q':
                    break
                if entry_choice == 'a':
                    prompt.add_student()
                elif entry_choice == 'd':
                    prompt.del_student()
                elif entry_choice == 'f':
                    data_methods.display()
                elif entry_choice == 'r':
                    file_methods.read_update_files()
                else:
                    print("Invalid input, try again")

            print('You have successfully left the program')
        
        except FileNotFoundError:
            if not os.path.isfile('register.txt'):
                file_methods.create_file('register.txt')

            if not os.path.isfile('attended.txt'):
                file_methods.create_file('attended.txt')
                initialized_total_attended = data_methods.create_dictionary()
                file_methods.append_file('attended.txt', str(initialized_total_attended))

            if not os.path.isfile('classes.txt'):
                file_methods.create_file('classes.txt')
                file_methods.append_file('classes.txt', str(0))

            if not os.path.isfile('percentage.txt'):
                file_methods.create_file('percentage.txt')
                initialized_percentage = data_methods.create_dictionary()
                file_methods.append_file('percentage.txt', str(initialized_percentage))

            print("One or more system files were not found. They have all been created with no data in them. You may now use the program, add students first using option 'a' to continue.")
            return actions.code_runner()

actions.code_runner()
