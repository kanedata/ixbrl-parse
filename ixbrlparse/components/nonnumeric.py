class ixbrlNonNumeric:

    def __init__(self, context, name, format_, value):

        name = name.split(":", maxsplit=1)
        if len(name) == 2:
            self.schema = name[0]
            self.name = name[1]
        else:
            self.schema = 'unknown'
            self.name = name[0]

        self.context = context
        self.format = format_
        self.value = value

    def to_json(self):
        values = self.__dict__
        values['context'] = self.context.to_json()
        return values
