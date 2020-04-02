from infrastructure.decorators import infrastructure


@infrastructure(order=1)
def order_one():
    pass


@infrastructure(order=2)
def order_two():
    pass


@infrastructure(order=1)
def order_duplicate_one():
    pass
