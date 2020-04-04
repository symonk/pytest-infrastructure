from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from threading import current_thread
from types import FunctionType
from typing import Any
from infrastructure import logger


@dataclass
class ScheduledResult:
    fx: FunctionType
    result: None


class FunctionScheduler:
    """
    This class is responsible for the actual execution of the infrastructure functions
    including the threaded-ness of such execution.  Internals of this class are to be scoped out
    and we have various edge cases to both identify and test
    """

    def __init__(self, executable_functions, thread_count):
        self.thread_count = thread_count
        self.parallel_functions, self.isolated_functions = executable_functions
        self.results = []
        self.isolated_results = []
        self.parallel_results = []

    def execute_functions(self) -> None:
        """
        Entry point for the scheduler to begin doing its work, here it will manage execution keeping track of
        exceptions and smartly managing both thread safe parallel and isolated runs
        """
        if self.isolated_functions:
            logger.info(
                f"pytest-infrastructure is executing sequential non thread-safe functions now..."
            )
        for function in self.isolated_functions:
            self.execute_function(function)

        if self.parallel_functions:
            logger.info(
                f"pytest-infrastructure is executing parallel thread-safe functions now"
            )

            tracker = {}
            with ThreadPoolExecutor() as executor:
                for func in self.parallel_functions:
                    tracker[func] = executor.submit(self.execute_function, func)

            for func, handler in zip(
                tracker.keys(), as_completed([tracker[k] for k in tracker.keys()])
            ):
                self.results.append(ScheduledResult(func, handler.result()))

        self.parallel_results = [
            result for result in self.results if not result.fx.meta_data.isolated
        ]

    def report_summary(self):
        if self.isolated_results:
            for item in self.isolated_results:
                logger.info(item)
        else:
            logger.info(f"pytest-validate never ran any isolated functions")

        if self.parallel_results:
            for item in self.isolated_results:
                logger.info(item)
        else:
            logger.info(f"pytest-validate never ran any parallel functions")

    @logger.catch
    def execute_function(self, function) -> Any:
        """
        Responsible for taking a single function and executing it
        note: this is not responsible for thread management, this is done prior and dispatched to this function
        """
        current_thread().name = f"{function.meta_data.name}"
        logger.info(f"Executing {function.meta_data.name}")
        try:
            result = function()
        except:  # noqa
            return result
