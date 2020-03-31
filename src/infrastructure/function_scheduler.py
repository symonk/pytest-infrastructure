from concurrent.futures.thread import ThreadPoolExecutor
from threading import current_thread
from typing import Any

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
        if self.isolated_functions:
            logger.info(
                f"pytest-infrastructure is executing sequential non thread-safe functions now..."
            )
        for function in self.isolated_functions:
            function()

        if self.parallel_functions:
            logger.info(
                f"pytest-infrastructure is executing parallel thread-safe functions now"
            )
        for function in self.parallel_functions:
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.execute_function, function)]
                logger.info(futures)

    @logger.catch
    def execute_function(self, function) -> Any:
        """
        Responsible for taking a single function and executing it
        note: this is not responsible for thread management, this is done prior and dispatched to this function
        """
        current_thread().name = f"{function.__name__}"
        logger.info(f"Executing {function.meta_data}")
        return function()
