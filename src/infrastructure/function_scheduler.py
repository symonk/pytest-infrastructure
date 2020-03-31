from infrastructure import logger


class FunctionScheduler:
    """
    This class is responsible for the actual execution of the infrastructure functions
    including the threaded-ness of such execution.  Internals of this class are to be scoped out
    and we have various edge cases to both identify and test
    """

    def __init__(self, executable_functions):
        self.parallel_functions, self.isolated_functions = executable_functions

    def begin_workload(self) -> None:
        """
        Entry point for the scheduler to begin doing its work, here it will manage execution keeping track of
        exceptions and smartly managing both thread safe parallel and isolated runs
        """
        for functions in self.parallel_functions, self.isolated_functions:
            for function in functions:
                self.execute_function(function)  # dummy for now until implemented!

    @logger.catch
    def execute_function(self, function) -> None:
        """
        Responsible for taking a single function and executing it
        note: this is not responsible for thread management, this is done prior and dispatched to this function
        """
        function()
