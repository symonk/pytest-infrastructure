from infrastructure.decorators import infrastructure


@infrastructure(isolated=True)
def validate_function_1():
    raise Exception("exception!")


@infrastructure(isolated=True)
def validate_function_2():
    pass


@infrastructure()
def validate_function_3():
    pass


@infrastructure()
def validate_function_4():
    pass
