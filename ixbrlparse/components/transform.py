from copy import deepcopy


class ixbrlFormat:
    """Base class for all iXBRL formats

    By default it attempts to convert a string to numbers by removing
    commas and spaces, and then converting to a float. It also supports
    negative numbers and scaling.

    Attributes:
        format (str): The name of the format of the numeric element
        decimals (int): The number of decimal places of the numeric element
        scale (int): The scale of the numeric element. The scale is represented
            as a power of 10. For example, a scale of 3 would mean that the
            value should be multiplied by 1000.
        sign (str): The sign of the numeric element. If sign is "-", then
            the value is multiplied by -1
    """

    def __init__(self, format_, decimals, scale, sign):

        if decimals.lower() == "inf":
            self.decimals = None
        else:
            self.decimals = int(decimals)

        self.format = None
        if format_:
            format_ = format_.split(":")
            if len(format_) > 1:
                self.format = ":".join(format_[1:])
                self.namespace = format_[0]
            else:
                self.format = ":".join(format_)
                self.namespace = None

        self.scale = int(scale)
        self.sign = sign

    def to_json(self):
        return deepcopy(self.__dict__)

    def parse_value(self, value):
        """Converts a string to a number

        Args:
            value (str): The string to convert

        Returns:
            float: The converted value
        """

        if isinstance(value, (int, float)):
            return value

        if value in ("-", ""):
            return 0

        value = value.replace(" ", "")
        value = value.replace(",", "")
        value = float(value)

        if self.sign == "-":
            value = value * -1

        if self.scale != 0:
            value = value * (10**self.scale)

        return value


class ixtZeroDash(ixbrlFormat):
    """Models a zero numeric element in an iXBRL document

    Always returns 0

    Attributes:
        dictionary containing the following keys:
            context (ixbrlContext): The context of the numeric element
            name (str): The name of the numeric element
            format (ixbrlFormat): The format of the numeric element
            value (float): The value of the numeric element
            unit (str): The unit of the numeric element
            text (str): The text of the numeric element
    """

    def parse_value(self, value):
        """Converts a string to a number

        Args:
            value (str): The string to convert

        Returns:
            int: The converted value (always 0)
        """
        return 0


class ixtNoContent(ixbrlFormat):
    """Models a no content numeric element in an iXBRL document

    Always returns None

    Attributes:
        dictionary containing the following keys:
            context (ixbrlContext): The context of the numeric element
            name (str): The name of the numeric element
            format (ixbrlFormat): The format of the numeric element
            value (float): The value of the numeric element
            unit (str): The unit of the numeric element
            text (str): The text of the numeric element
    """

    def parse_value(self, value):
        """Converts a string to a number

        Args:
            value (str): The string to convert

        Returns:
            None: The converted value (always None)
        """
        return None


class ixtFixedFalse(ixbrlFormat):
    """Models a fixed false numeric element in an iXBRL document

    Always returns False

    Attributes:
        dictionary containing the following keys:
            context (ixbrlContext): The context of the numeric element
            name (str): The name of the numeric element
            format (ixbrlFormat): The format of the numeric element
            value (float): The value of the numeric element
            unit (str): The unit of the numeric element
            text (str): The text of the numeric element
    """

    def parse_value(self, value):
        """Converts a string to a number

        Args:
            value (str): The string to convert

        Returns:
            bool: The converted value (always False)
        """
        return False


class ixtFixedTrue(ixbrlFormat):
    """Models a fixed true numeric element in an iXBRL document

    Always returns True

    Attributes:
        dictionary containing the following keys:
            context (ixbrlContext): The context of the numeric element
            name (str): The name of the numeric element
            format (ixbrlFormat): The format of the numeric element
            value (float): The value of the numeric element
            unit (str): The unit of the numeric element
            text (str): The text of the numeric element
    """

    def parse_value(self, value):
        """Converts a string to a number

        Args:
            value (str): The string to convert

        Returns:
            bool: The converted value (always True)
        """
        return True


class ixtNumComma(ixbrlFormat):
    """Models a comma separated numeric element in an iXBRL document

    This element is used for numbers where a comma is used as the decimal
    separator. For example, 100,00 would be converted to 100.00.

    It also assumes that any full stops are used as thousands separators.
    For example, 1.000,00 would be converted to 1000.00.

    Attributes:
        dictionary containing the following keys:
            context (ixbrlContext): The context of the numeric element
            name (str): The name of the numeric element
            format (ixbrlFormat): The format of the numeric element
            value (float): The value of the numeric element
            unit (str): The unit of the numeric element
            text (str): The text of the numeric element
    """

    def parse_value(self, value):
        """Converts a string to a number

        First removes any full stops, and then replaces any commas with
        full stops. It then converts the string to a float.

        Args:
            value (str): The string to convert

        Returns:
            float: The converted value
        """
        value = value.replace(".", "")
        value = value.replace(",", ".")
        return super().parse_value(value)


class ixtNumWordsEn(ixbrlFormat):
    """Models a numeric element in an iXBRL document that is written in words

    Uses the [word2number](https://pypi.org/project/word2number/) library to
    convert the words to a number.

    Attributes:
        dictionary containing the following keys:
            context (ixbrlContext): The context of the numeric element
            name (str): The name of the numeric element
            format (ixbrlFormat): The format of the numeric element
            value (float): The value of the numeric element
            unit (str): The unit of the numeric element
            text (str): The text of the numeric element
    """

    def parse_value(self, value):
        """Converts a string to a number

        Args:
            value (str): The string to convert

        Returns:
            float: The converted value
        """
        value = value.lower()
        if value in ("no", "none"):
            return 0
        from word2number import w2n

        return w2n.word_to_num(value)


def get_format(format_):
    """Returns the correct format class for the given format

    Only particular formats are supported. If the format is not supported
    then a NotImplementedError is raised."""

    original_format = format_

    if format_ is None:
        return ixbrlFormat

    format_ = format_.split(":")
    if len(format_) > 1:
        namespace = format_[0]
        format_ = ":".join(format_[1:])
    else:
        namespace = None
        format_ = ":".join(format_)

    format_ = format_.replace("-", "")

    if format_ in ("zerodash", "numdash", "fixedzero"):
        return ixtZeroDash

    if format_ in ("nocontent", "fixedempty"):
        return ixtNoContent

    if format_ in ("booleanfalse", "fixedfalse"):
        return ixtFixedFalse

    if format_ in ("booleantrue", "fixedtrue"):
        return ixtFixedTrue

    if format_ in ("numdotdecimal", "numcommadot", "numspacedot"):
        return ixbrlFormat

    if format_ in ("numcomma", "numdotcomma", "numspacecomma", "numcommadecimal"):
        return ixtNumComma

    if format_ == "numwordsen":
        return ixtNumWordsEn

    raise NotImplementedError(
        'Format "{}" not implemented (namespace "{}")'.format(
            original_format,
            namespace,
        )
    )
