from multiprocessing import Process
from typing import NoReturn

class Process_Manager:
    def __init__(self):
        self.process: list[Process] = []
    
    def new_process(self, target, args: tuple = ()) -> NoReturn:
        self.process.append(Process(target=target, args=args))
        self.process[-1].start()

    def __getitem__(self, index: int) -> Process:
        return self.process[index]