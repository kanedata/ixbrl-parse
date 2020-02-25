from .transform import get_format

class ixbrlNumeric:

    # contextref
    # decimals
    # format
    # name
    # scale
    # sign
    # text
    # unitref
    # xmlns:ix
    def __init__(self, attrs):
        name = attrs.get('name', "").split(":", maxsplit=1)
        if len(name) == 2:
            self.schema = name[0]
            self.name = name[1]
        else:
            self.schema = 'unknown'
            self.name = name[0]

        self.text = attrs.get('value', attrs.get('text'))
        self.context = attrs.get('context')
        self.unit = attrs.get('unit')

        format_ = {
            "format_": attrs.get('format'),
            "decimals": attrs.get('decimals', "0"),
            "scale": attrs.get('scale', 0),
            "sign": attrs.get('sign', ""),
        }
        self.format = get_format(format_['format_'])(**format_)

        try:
            self.value = self.format.parse_value(self.text)
        except ValueError:
            print(attrs)
            raise

    def to_json(self):
        values = self.__dict__
        values['context'] = self.context.to_json()
        return values
