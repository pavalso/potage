def traverse_subclasses(cls) -> list:
    if not hasattr(cls, "__subclasses__"):
        return []

    subclasses: list = cls.__subclasses__()

    for subclass in cls.__subclasses__():
        subclasses.extend(traverse_subclasses(subclass))

    return subclasses
