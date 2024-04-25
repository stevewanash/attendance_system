import unittest
from unittest.mock import patch
import models.attendance
from io import StringIO
import sys

class TestPercentageCalc(unittest.TestCase):
    
    def test_percentage_calc(self):
        # Test case for the percentage_calc function
        # Test if the percentage calculation is accurate
        percentage_dict = {}
        attendance_dict = {
            'John': 5,
            'Jane': 3,
            'Mike': 8
        }
        total_classes = 10

        models.attendance.calculation.percentage_calc(percentage_dict, attendance_dict, 'John', total_classes)
        models.attendance.calculation.percentage_calc(percentage_dict, attendance_dict, 'Jane', total_classes)
        models.attendance.calculation.percentage_calc(percentage_dict, attendance_dict, 'Mike', total_classes)

        self.assertEqual(percentage_dict['John'], 50.0)
        self.assertEqual(percentage_dict['Jane'], 30.0)
        self.assertEqual(percentage_dict['Mike'], 80.0)

class TestCodeRunner(unittest.TestCase):

    @patch('builtins.input', side_effect=['a', 'celine123', 'celine', 'q'])
    def test_code_runner_name_add_with_wrong_input(self, mock_input):
        # Test the code_runner function with valid inputs to cover the main functionality
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'The student name needs to be a string with only alphabets, try again')
        self.assertEqual(captured_output.getvalue().splitlines()[1].strip(), 'celine has been added to your register')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')

    @patch('builtins.input', side_effect=['x', 'q'])
    def test_code_runner_with_invalid_input(self,mock_input):
        # Test the code_runner function with invalid input to check the error handling
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'Invalid input, try again')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')

    @patch('builtins.input', side_effect=['d', 'celine234', 'celine', 'q'])
    def test_code_runner_name_delete_with_wrong_input(self, mock_input):
        # Test the code_runner function with inputs in caps
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'The student name needs to be a string with only alphabets, try again')
        self.assertEqual(captured_output.getvalue().splitlines()[1].strip(), 'celine has been removed from your register')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')


    @patch('builtins.input', side_effect=['123', 'q'])
    def test_code_runner_with_numerical_input(self, mock_input):
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'Invalid input, try again')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')

    @patch('builtins.input', side_effect=['!@#$', 'q'])
    def test_code_runner_with_non_alphanumeric_input(self, mock_input):
        # Test the code_runner function with non-alphanumeric input
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'Invalid input, try again')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')

    @patch('builtins.input', side_effect=['  A  ', ' steve', 'D ', ' steve', ' Q'])
    def test_code_runner_with_whitespace_input(self, mock_input):
        # Test the code_runner function with inputs with whitespaces on either end
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'steve has been added to your register')
        self.assertEqual(captured_output.getvalue().splitlines()[1].strip(), 'steve has been removed from your register')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')

    @patch('builtins.input', side_effect=['a', 'steve', 'a', 'steve', 'd', 'steve', ' Q'])
    def test_code_runner_with_duplicate_added_names(self, mock_input):
        # Test the code_runner function with inputs with whitespaces on either end
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'steve has been added to your register')
        self.assertEqual(captured_output.getvalue().splitlines()[1].strip(), 'steve is already in your register')
        self.assertEqual(captured_output.getvalue().splitlines()[2].strip(), 'steve has been removed from your register')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')

    @patch('builtins.input', side_effect=['d', 'matt', 'a', 'matt', 'd', 'matt', ' Q'])
    def test_code_runner_with_non_existent_delete_names(self, mock_input):
        # Test the code_runner function with inputs with whitespaces on either end
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'matt is not in your register')
        self.assertEqual(captured_output.getvalue().splitlines()[1].strip(), 'matt has been added to your register')
        self.assertEqual(captured_output.getvalue().splitlines()[2].strip(), 'matt has been removed from your register')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')


    @patch('builtins.input', side_effect=['Hello', 'Q'])
    def test_code_runner_with_long_string_input(self, mock_input):
        # Test the code_runner function with strings with more than one alphabet
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'Invalid input, try again')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')

    @patch('builtins.input', side_effect=['', 'Q'])
    def test_code_runner_with_empty_string_input(self, mock_input):
        # Test the code_runner function with an empty string input
        captured_output = StringIO()
        sys.stdout = captured_output
        models.attendance.actions.code_runner()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().splitlines()[0].strip(), 'Invalid input, try again')
        self.assertEqual(captured_output.getvalue().splitlines()[-1].strip(), 'You have successfully left the program')

if __name__ == '__main__':
    unittest.main()