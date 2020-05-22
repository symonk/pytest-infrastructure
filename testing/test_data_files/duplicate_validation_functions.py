from infrastructure.decorators import infrastructure


@infrastructure()
def this_was_duplicated():
    pass


@infrastructure()
def this_was_duplicated():
    pass
