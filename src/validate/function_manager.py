from typing import Tuple


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
            self.raw_functions,
            self.raw_functions,
        )  # dummy for now until implemented

    def _order_usable_functions(self):
        """
        Order the functions as best as possible in each retrospective list
        note: functions decorated with thread_safe=True will NOT account for ordering as by nature they are
        all ran together
        """
        pass

    @staticmethod
    def _strip_meta_data_from_function(function) -> Tuple:
        """
        Strip the meta data from our validate functions, presenting it an an un-packable format for easy use
        :param function: the validate decorated function to retrieve meta data from
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
