import subprocess
import os
class CodeRunner:
    FILE_DEFAULT_NAME = "runnable.py"
    TEST_DEFAULT_NAME = "test.py"
    TEST_DEFAULT_PATH = "tests/"
    SOLUTIONS_DEFAULT_PATH = "files/"
    DEFAULT_TIMEOUT = 3
    @classmethod
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
        cls.add_file(code)
        returncode, output, error = cls.__run(cls.FILE_DEFAULT_NAME)
        return (returncode, output, error)
    @classmethod
    def add_file(cls, code: str):
        with open("./files/" + cls.FILE_DEFAULT_NAME, "w") as file:
            file.write(code)
        pass
    
    @classmethod
    def test_code(cls, code: str, test_name: str):
        try: 
            data = None
            with open(cls.TEST_DEFAULT_PATH + test_name, "r") as file:
                data = file.read()
            with open(cls.SOLUTIONS_DEFAULT_PATH + cls.TEST_DEFAULT_NAME, "w") as file:
                file.write(data)
            cls.add_file(code)
            return_code, output, error = cls.__run(cls.TEST_DEFAULT_NAME)
            return (return_code, output, error)
        except FileNotFoundError:
            return (-1, "", "Server Error: Test file Not Found")
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
