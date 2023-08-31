class DataToItemError(ValueError):
    "Raise when converting data to item failed"


class KeyFoundError(ValueError):
    """Typically raised in insertion.

    Raised when an item for given key/id field
    is found when it was not expected.

    """


class ItemNotFoundError(ValueError):
    "Raise when item not found"
