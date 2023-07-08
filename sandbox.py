import subprocess
import os
import uuid
import re
class CodeRunner:
    FILE_DEFAULT_NAME = "runnable.py"
    TEST_DEFAULT_NAME = "test.py"
    TEST_DEFAULT_PATH = "tests/"
    FILE_DEFAULT_PREVENT = "prevent.py"
    FILE_DEFAULT_UNPREVENT = "unprevent.py"
    SOLUTIONS_DEFAULT_PATH = "files/"
    DEFAULT_TIMEOUT = os.environ.get("DEFAULT_TIMEOUT") if os.environ.get("DEFAULT_TIMEOUT") else 5
    INPUT_REGEX = r"input\s{0,1}\("
    @classmethod
    def defend_from_bad_activity(cls, code: str):
        return (True, "")

    @classmethod
    def check_for_input(cls, code: str):
        match = re.search(cls.INPUT_REGEX, code)
        if match:
            return True
        return False
    def __run(cls, filename: str):
        try:
            result = subprocess.run(["python", "files/" + filename ], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                    universal_newlines=True, timeout=cls.DEFAULT_TIMEOUT)
            stdout_output = result.stdout
            stderr_output = result.stderr
            return_code = result.returncode
            return (return_code, stdout_output, stderr_output)
        except subprocess.TimeoutExpired:
            return (-1, "", "Timeout excedeed")
    @classmethod
    def run_code(cls, code: str):
        check = cls.defend_from_bad_activity(code)
        if check[0] == True: 
            # if everything is good
            prevent_content = ""
            with open(cls.SOLUTIONS_DEFAULT_PATH + cls.FILE_DEFAULT_PREVENT, "r") as prevent_file:
                prevent_content = prevent_file.read()
            cls.add_file(prevent_content + "\n" + code)
            if cls.check_for_input(code):
                return (0, "", "", uuid.uuid4())
            returncode, output, error = cls.__run(cls.FILE_DEFAULT_NAME)
            return (returncode, output, error, None)
        else:
            return (-1, "", check[1])
    @classmethod
    def add_file(cls, code: str):
        with open("./files/" + cls.FILE_DEFAULT_NAME, "w") as file:
            file.write(code)
        pass
    @classmethod
    def add_to_file(cls, code: str):
        with open("./files/" + cls.FILE_DEFAULT_NAME, "a") as file:
            file.write("\n" + code)
    @classmethod
    def test_code(cls, code: str, test_name: str):
        check = cls.defend_from_bad_activity(code)
        if check[0] == True:
            try: 
                test_code = ""
                prevent_code = ""
                unprevent_code = ""
                with open(cls.SOLUTIONS_DEFAULT_PATH + cls.FILE_DEFAULT_PREVENT) as prevent_file:
                    prevent_code = prevent_file.read()
                with open(cls.TEST_DEFAULT_PATH + test_name, "r") as test_file:
                    test_code = test_file.read()
                with open(cls.SOLUTIONS_DEFAULT_PATH + cls.FILE_DEFAULT_UNPREVENT) as unprevent_file:
                    unprevent_code = unprevent_file.read()
                cls.add_file(prevent_code + "\n" + code + "\n" + unprevent_code + "\n" + test_code)
                return_code, output, error = cls.__run(cls.TEST_DEFAULT_NAME)
                return (return_code, output, error)
            except FileNotFoundError:
                return (-1, "", "Server Error: Test file Not Found")
        else:
            return (-1, "", check[1])
        
    @classmethod
    def add_test_file(cls, fileb: bytes, filename: str):
        try:
            with open(cls.TEST_DEFAULT_PATH + filename, "wb") as file:
                file.write(fileb)
            return True
        except:
            return False
    @classmethod
    def list_test_files(cls):
        try:
            files = os.listdir("./tests/")
            for i in files:
                if i == "runnable.py":
                    files.remove(i)
            return files
        except:
            return None
