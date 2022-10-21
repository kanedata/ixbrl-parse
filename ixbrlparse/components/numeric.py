from copy import deepcopy

from .transform import get_format, ixbrlFormat


class ixbrlNumeric:
    """Models a numeric element in an iXBRL document

    Attributes:
        dictionary containing the following keys:
            context (ixbrlContext): The context of the numeric element
            name (str): The name of the numeric element
            format (ixbrlFormat): The format of the numeric element
            value (float): The value of the numeric element
            unit (str): The unit of the numeric element
            text (str): The text of the numeric element"""

    def __init__(self, attrs):
        name = attrs.get("name", "").split(":", maxsplit=1)
        if len(name) == 2:
            self.schema = name[0]
            self.name = name[1]
        else:
            self.schema = "unknown"
            self.name = name[0]

        self.text = attrs.get("value", attrs.get("text"))
        self.context = attrs.get("context")
        self.unit = attrs.get("unit")

        format_ = {
            "format_": attrs.get("format"),
            "decimals": attrs.get("decimals", "0"),
            "scale": attrs.get("scale", 0),
            "sign": attrs.get("sign", ""),
        }
        self.format = get_format(format_["format_"])(**format_)

        try:
            self.value = self.format.parse_value(self.text)
        except ValueError:
            print(attrs)
            raise

    def to_json(self):
        values = deepcopy(self.__dict__)
        if isinstance(values.get("format"), ixbrlFormat):
            values["format"] = values["format"].to_json()
        values["context"] = self.context.to_json()
        return values
