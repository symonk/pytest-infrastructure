from typing import Tuple, List, Optional


class FunctionManager:
    """
    A class responsible for providing all logic to the functions in order to determine some of the following:
    should they be executed?
    should they be threaded?
    what order should they be in?
    """

    def __init__(self, unfiltered_functions: List, environment: str = ""):
        self.unfiltered_functions: List = unfiltered_functions
        self.filtered_functions: List = []
        self.environment: str = environment
        self.parallel_functions: Optional[List] = []
        self.isolated_functions: Optional[List] = []
        self.disabled_functions = []

    def organize_functions(self):
        """
        Organize the function(s) into two separate lists, thread-parallel safe functions
        and isolated functions. adhering to order.  disabled functions should never be added and functions
        marked not to run on the environment provided should also be never returned
        """
        self._manage_function_disablement()
        self._remove_non_environmentally_friendly_functions()
        self._order_usable_functions()
        print(
            f"pytest-infrastructure will attempt to execute the following functions sequentially:"
        )
        for fx in self.isolated_functions:
            print(f"function: {fx.meta_data}")

        print(
            f"pytest-infrastructure will attempt to execute the following functions in parallel:"
        )
        for fx in self.parallel_functions:
            print(f"function: {fx.meta_data}")

    def _manage_function_disablement(self):
        """
        Given an appropriate environment and functions enabled= state; remove them completely from runnable functions
        """
        print(
            f"pytest-infrastructure is disabling functions from executing where appropriate"
        )

        for fx in self.unfiltered_functions:
            if not fx.meta_data.enabled or (
                fx.meta_data.not_on_env
                and self.environment.lower()
                not in [env.lower() for env in fx.meta_data.not_on_env]
            ):
                self.disabled_functions.append(fx)
                print(
                    f"function {fx.meta_data.name} was disabled due to enabled=False or not_on_env not succesful "
                    f"meta data of the function was: {fx.meta_data} and environment was: {self.environment}"
                )
            else:
                self.filtered_functions.append(fx)

        print(
            f"pytest-validate has deregistered a total of len{self.disabled_functions} functions"
        )

    def _remove_non_environmentally_friendly_functions(self):
        """
        Remove any functions from self.parallel_functions where the function meta data indicates a disabled function
        Remove any functions from self.isolated_functions where the function meta data does not match a specified env
        """
        (self.parallel_functions, self.isolated_functions) = (
            [func for func in self.filtered_functions if not func.meta_data.isolated],
            [func for func in self.filtered_functions if func.meta_data.isolated],
        )  # dummy for now until implemented

    def _order_usable_functions(self):
        """
        Order the functions as best as possible in each retrospective list
        note: functions decorated with thread_safe=True will NOT account for ordering as by nature they are
        all ran together
        """
        if self.isolated_functions:
            print(f"reshuffling order to detect any negatively ordered functions")
            for fx in self.isolated_functions:
                if fx.meta_data.order < 0:
                    fx.meta_data.order = 0

            print(
                f"current order of functions collected is {[fx.meta_data.order for fx in self.isolated_functions]}"
                f"pytest-infrastructure is applying execution order now...."
            )
            self.isolated_functions.sort(
                key=lambda func_dataclass: func_dataclass.meta_data.order
            )
            print(
                f"functions have been sorted, execution for isolated functions is as follows:"
            )
            for fx in self.isolated_functions:
                print(
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
            function.meta_data.not_on_env,
            function.meta_data.isolated,
        )
