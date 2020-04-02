from infrastructure.decorators import infrastructure


@infrastructure(isolated=False)
def do_one():
    pass


@infrastructure(isolated=False)
def do_two():
    pass


@infrastructure(isolated=False)
def do_three():
    pass
