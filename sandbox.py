import subprocess
import os
import uuid
import re
import json
from config import Config
class CodeRunner:
    FILE_DEFAULT_NAME = "runnable.py"
    TEST_DEFAULT_NAME = "test.py"
    TEST_DEFAULT_PATH = "tests/"
    FILE_DEFAULT_PREVENT = "prevent.py"
    FILE_DEFAULT_UNPREVENT = "unprevent.py"
    SOLUTIONS_DEFAULT_PATH = "files/"
    DEFAULT_TIMEOUT = 5
    INPUT_REGEX = r"input\s{0,1}\("
    SECRET = "C7SNKxm9knQd3r9xyC8qDNTm65wAY8fNhDzF"
    def __init__(self, config: Config):
        self.DEFAULT_TIMEOUT = config.timeout
        self.update_prevent(config.granted_modules)
    
    def update_prevent(self, modules: list):
        prevent_material_data = ""
        with open("./files/prevent_material.py") as prevent_material:
            prevent_material_data = prevent_material.read()
        
        prevent_material_data = prevent_material_data.replace("granted_modules", str(modules))

        injected_string = "import sys\n"

        with open("./files/prevent.py", "w") as prevent:
            prevent.write(injected_string + prevent_material_data)


    def defend_from_bad_activity(self, output: str):
        # check if the user finds the real input
        if self.SECRET in output :
            return output.replace(self.SECRET, "")
        return output

    def check_for_input(self, code: str):
        match = re.search(self.INPUT_REGEX, code)
        if match:
            return True
        return False
    
    def __run(self, filename: str):
        try:
            result = subprocess.run(["python", "files/" + filename ], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                    universal_newlines=True, timeout=self.DEFAULT_TIMEOUT)
            stdout_output = result.stdout
            stderr_output = result.stderr
            return_code = result.returncode
            return (return_code, stdout_output, stderr_output)
        except subprocess.TimeoutExpired:
            return (-1, "", "Timeout excedeed")

    def run_code(self, code: str):
        # if everything is good
        prevent_content = ""
        with open(self.SOLUTIONS_DEFAULT_PATH + self.FILE_DEFAULT_PREVENT, "r") as prevent_file:
            prevent_content = prevent_file.read()
        self.add_file(prevent_content + "\n" + code)
        if self.check_for_input(code):
            return (0, "", "", uuid.uuid4())
        returncode, output, error = self.__run(self.FILE_DEFAULT_NAME)
        return (returncode, output, error, None)
        
    def add_file(self, code: str):
        with open("./files/" + self.FILE_DEFAULT_NAME, "w") as file:
            file.write(code)
        pass
    
    def add_to_file(self, code: str):
        with open("./files/" + self.FILE_DEFAULT_NAME, "a") as file:
            file.write("\n" + code)
    
    def test_code(self, code: str, test_name: str):
        check = self.defend_from_bad_activity(code)
        if check[0] == True:
            try: 
                test_code = ""
                prevent_code = ""
                unprevent_code = ""
                with open(self.SOLUTIONS_DEFAULT_PATH + self.FILE_DEFAULT_PREVENT) as prevent_file:
                    prevent_code = prevent_file.read()
                with open(self.TEST_DEFAULT_PATH + test_name, "r") as test_file:
                    test_code = test_file.read()
                with open(self.SOLUTIONS_DEFAULT_PATH + self.FILE_DEFAULT_UNPREVENT) as unprevent_file:
                    unprevent_code = unprevent_file.read()
                self.add_file(prevent_code + "\n" + code + "\n" + unprevent_code + "\n" + test_code)
                return_code, output, error = self.__run(self.TEST_DEFAULT_NAME)
                return (return_code, output, error)
            except FileNotFoundError:
                return (-1, "", "Server Error: Test file Not Found")
        else:
            return (-1, "", check[1])
        
    def add_test_file(self, fileb: bytes, filename: str):
        try:
            with open(self.TEST_DEFAULT_PATH + filename, "wb") as file:
                file.write(fileb)
            return True
        except:
            return False
    
    def list_test_files(self):
        try:
            files = os.listdir("./tests/")
            for i in files:
                if i == "runnable.py":
                    files.remove(i)
            return files
        except:
            return None
