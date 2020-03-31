from infrastructure import validate


@validate()
def validate_raises_ex():
    raise Exception("something went horribly wrong")
