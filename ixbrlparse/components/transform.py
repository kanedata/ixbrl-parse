from copy import deepcopy
from typing import List, Optional, Type, Union

from .functionixt import ixtNamespaceFunctions


class ixbrlFormat:
    def __init__(
        self,
        format_: str,
        decimals: Optional[Union[int, str]],
        scale: Union[int, str] = 1,
        sign: Optional[str] = None,
        ixt: Optional[str] = None,
    ) -> None:

        if isinstance(decimals, str):
            if decimals.lower() == "inf":
                self.decimals = None
            else:
                self.decimals = int(decimals)

        self.format: Optional[str] = None
        self.namespace: Optional[str] = None
        if format_:
            format_array: List[str] = format_.split(":")
            if len(format_array) > 1:
                self.format = ":".join(format_array[1:])
                self.namespace = format_array[0]
            else:
                self.format = ":".join(format_array)
                self.namespace = None

        self.scale = int(scale)
        self.sign = sign
        self.ixt = ixt

    def to_json(self):
        return deepcopy(self.__dict__)

    def parse_value(
        self, value: Union[str, int, float]
    ) -> Optional[Union[int, float, bool, str]]:

        if isinstance(value, (int, float, str)):
            return value

        if isinstance(value, str):
            if value in ("-", ""):
                return 0

            value_numeric: float = float(value.replace(" ", "").replace(",", ""))

            if self.sign == "-":
                value_numeric = value_numeric * -1

            if self.scale != 0:
                value_numeric = value_numeric * (10**self.scale)

            return value_numeric


class ixtZeroDash(ixbrlFormat):
    def parse_value(self, value: Union[str, int, float]) -> Union[int, float]:
        return 0


class ixtNoContent(ixbrlFormat):
    def parse_value(self, value: Union[str, int, float]) -> None:
        return None


class ixtFixedFalse(ixbrlFormat):
    def parse_value(self, value: Union[str, int, float]) -> bool:
        return False


class ixtFixedTrue(ixbrlFormat):
    def parse_value(self, value: Union[str, int, float]) -> bool:
        return True


class ixtNumComma(ixbrlFormat):
    def parse_value(self, value: Union[str, int, float]) -> Optional[Union[int, float]]:
        if isinstance(value, str):
            value = value.replace(".", "")
            value = value.replace(",", ".")
        return super().parse_value(value)


class ixtNumWordsEn(ixbrlFormat):
    def parse_value(self, value: Union[str, int, float]) -> Optional[Union[int, float]]:
        if isinstance(value, str):
            value = value.lower()
            if value in ("no", "none"):
                return 0
            from word2number import w2n

            return w2n.word_to_num(value)
        return super().parse_value(value)


class ixtWrapper(ixbrlFormat):
    def parse_value(self, value):
        return ixtNamespaceFunctions[self.ixt][self.format](value)


def get_format(format_: Optional[str]) -> Type[ixbrlFormat]:

    if not isinstance(format_, str):
        return ixbrlFormat

    original_format: str = format_

    format_list: List = format_.split(":")
    if len(format_list) > 1:
        namespace = format_list[0]
        format_ = ":".join(format_list[1:])
    else:
        namespace = None
        format_ = ":".join(format_list)

    format_ = format_.replace("-", "")

    if format_ == "numwordsen":
        return ixtNumWordsEn
    elif format_:
        return ixtWrapper

    raise NotImplementedError(
        'Format "{}" not implemented (namespace "{}")'.format(
            original_format,
            namespace,
        )
    )
