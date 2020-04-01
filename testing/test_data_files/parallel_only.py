from infrastructure import validate


@validate(isolated=False)
def do_one():
    pass


@validate(isolated=False)
def do_two():
    pass


@validate(isolated=False)
def do_three():
    pass
