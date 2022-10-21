from copy import deepcopy


class ixbrlNonNumeric:
    """Models a non-numeric element in an iXBRL document

    Non-numeric elements are used to store information such as the name of the
    entity, the name of the reporting period, etc.

    The value of non-numeric elements is always a string, so we don't need to
    worry about parsing the string.

    Attributes:
        context (ixbrlContext): The context of the non-numeric element
        name (str): The name of the non-numeric element
        format (str): The format of the non-numeric element
        value (str): The value of the non-numeric element"""

    def __init__(self, context, name, format_, value):

        name = name.split(":", maxsplit=1)
        if len(name) == 2:
            self.schema = name[0]
            self.name = name[1]
        else:
            self.schema = "unknown"
            self.name = name[0]

        self.context = context
        self.format = format_
        self.value = value

    def to_json(self):
        values = deepcopy(self.__dict__)
        values["context"] = self.context.to_json()
        return values
