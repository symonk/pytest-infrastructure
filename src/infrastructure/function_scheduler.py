import traceback
from concurrent.futures import as_completed
from infrastructure.plugin_utilities import infra_print

import pytest
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from threading import current_thread
from types import FunctionType
from typing import Any

from yaspin import yaspin


@dataclass
class ScheduledResult:
    fx: FunctionType
    exc_type: Exception = None
    exc_info: str = None

    def __repr__(self):
        return f"function: {self.fx.meta_data.name} | result: {self.exc_type} | traceback: {self.exc_info}"


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

    def execute_functions(self) -> None:
        """
        Entry point for the scheduler to begin doing its work, here it will manage execution keeping track of
        exceptions and smartly managing both thread safe parallel and isolated runs
        """
        for fx in self.isolated_functions:
            self.execute_sequential_function(fx)
        self.execute_parallel_functions(self.parallel_functions)

    def report_summary(self) -> None:
        """
        Responsible for outputting the results of all of the function execution
        """
        failures = [result for result in self.results if result.exc_info is not None]
        if failures:
            for failure in failures:
                infra_print(
                    f"Failure caused by: {failure.fx.meta_data.name} due to [{failure.exc_type}] \n "
                    f"{failure.exc_info}"
                )
            pytest.exit("deemed the run a failure; no tests will be collected", 5)

    def execute_sequential_function(self, fx) -> Any:
        """
        Responsible for taking a single function and executing it
        note: this is not responsible for thread management, this is done prior and dispatched to this function
        """
        infra_print("executing a function!")
        current_thread().name = f"{fx.meta_data.name}"
        scheduled = partial(ScheduledResult, fx)
        with yaspin() as spinner:
            try:
                fx()
                self.results.append(scheduled())
                spinner.ok("passed")
            except Exception as ex:  # noqa
                self.results.append(
                    scheduled(exc_type=type(ex), exc_info=(ex, traceback.format_exc()))
                )
                spinner.fail("failed")

    def execute_parallel_functions(self, fxs):
        """
        using a thread pool executor; submit the concurrent functions and keep record of results against the
        corresponding called function
        :param fxs: a list of functions to be submitted for concurrent execution
        """
        if not fxs:
            return
        future_tracker = {}
        with ThreadPoolExecutor(max_workers=len(fxs)) as executor:
            for fx in fxs:
                future_tracker[fx] = as_completed(
                    executor.submit(self.execute_sequential_function, fx)
                )
