from abc import ABC, abstractmethod


class Compiler(ABC):
    NAME = ''
    
    def __init__(self, version: str, compilation_flags: list, input_file_directory: str):
        if compilation_flags in ["", None]:
            compilation_flags = []
        self._version = version
        self._input_file_directory = input_file_directory
        self._compilation_flags = compilation_flags
        self.name = ''

    @abstractmethod
    def compile(self):
        """implement your own compiler"""
        pass

    def initiate_for_new_task(self, compilation_flags: list, input_file_directory: str, **kwargs):
        self.set_compilation_flags(compilation_flags)
        self.set_input_file_directory(input_file_directory)

    def get_version(self):
        return self._version

    def set_version(self, version: str):
        self._version = version

    def get_input_file_directory(self):
        return self._input_file_directory
    
    def set_input_file_directory(self, input_file_directory: str):
        self._input_file_directory = input_file_directory

    def get_compilation_flags(self):
        return self._compilation_flags

    def set_compilation_flags(self, compilation_flags: list):
        self._compilation_flags = compilation_flags
