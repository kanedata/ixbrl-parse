from copy import deepcopy


class ixbrlFormat:
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
    def parse_value(self, value):
        return 0


class ixtNoContent(ixbrlFormat):
    def parse_value(self, value):
        return None


class ixtFixedFalse(ixbrlFormat):
    def parse_value(self, value):
        return False


class ixtFixedTrue(ixbrlFormat):
    def parse_value(self, value):
        return True


class ixtNumComma(ixbrlFormat):
    def parse_value(self, value):
        value = value.replace(".", "")
        value = value.replace(",", ".")
        return super().parse_value(value)


class ixtNumWordsEn(ixbrlFormat):
    def parse_value(self, value):
        value = value.lower()
        if value in ("no", "none"):
            return 0
        from word2number import w2n

        return w2n.word_to_num(value)


def get_format(format_):

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
