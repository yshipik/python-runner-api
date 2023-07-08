from process import Process
class ProcessManager:
    processes: dict[str, Process]
    __instance = None
    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(ProcessManager)
        return cls.__instance

    def __init__(self):
        self.processes = {}