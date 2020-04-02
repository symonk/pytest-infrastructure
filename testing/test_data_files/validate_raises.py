from infrastructure.decorators import infrastructure


@infrastructure()
def validate_raises_ex():
    raise Exception("something went horribly wrong")
