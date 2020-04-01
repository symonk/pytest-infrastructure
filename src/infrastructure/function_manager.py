from typing import Tuple
from infrastructure import logger


class FunctionManager:
    """
    A class responsible for providing all logic to the functions in order to determine some of the following:
    should they be executed?
    should they be threaded?
    what order should they be in?
    """

    def __init__(self, functions, environment):
        self.raw_functions = functions
        self.environment = environment
        self.parallel_functions = None
        self.isolated_functions = None

    def organize_functions(self):
        """
        Organize the function(s) into two separate lists, thread-parallel safe functions
        and isolated functions. adhering to order.  disabled functions should never be added and functions
        marked not to run on the environment provided should also be never returned
        """
        self._remove_non_environmentally_friendly_functions()
        self._order_usable_functions()

    def _remove_non_environmentally_friendly_functions(self):
        """
        Remove any functions from self.parallel_functions where the function meta data indicates a disabled function
        Remove any functions from self.isolated_functions where the function meta data does not match a specified env
        """
        (self.parallel_functions, self.isolated_functions) = (
            [func for func in self.raw_functions if not func.meta_data.isolated],
            [func for func in self.raw_functions if func.meta_data.isolated],
        )  # dummy for now until implemented

    def _order_usable_functions(self):
        """
        Order the functions as best as possible in each retrospective list
        note: functions decorated with thread_safe=True will NOT account for ordering as by nature they are
        all ran together
        """
        breakpoint()
        if self.isolated_functions:
            logger.info(
                f"current order of functions collected is {[fx.order for fx in self.isolated_functions]}"
                f"pytest-infrastructure is applying execution order now...."
            )
            self.isolated_functions.sort(
                key=lambda func_dataclass: func_dataclass.order
            )
            logger.info(
                f"functions have been sorted, execution for isolated functions is as follows:"
            )
            for fx in self.isolated_functions:
                logger.info(
                    f"order => {fx.meta_data.order} ~ function => {fx.meta_data.name}"
                )

    @staticmethod
    def _strip_meta_data_from_function(function) -> Tuple:
        """
        Strip the meta data from our infrastructure functions, presenting it an an un-packable format for easy use
        :param function: the infrastructure decorated function to retrieve meta data from
        :return: a tuple of the meta data
        """
        return (
            function.meta_data.order,
            function.meta_data.enabled,
            function.meta_data.only_on_env,
            function.meta_data.isolated,
        )

    def yield_usable_functions(self) -> Tuple:
        return self.parallel_functions, self.isolated_functions
