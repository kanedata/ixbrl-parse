from copy import deepcopy
from datetime import date
from typing import List, Optional, Union


class ixbrlFormat:  # noqa: N801
    format_names: tuple[str, ...] = ()

    def __init__(
        self,
        format_: str,
        decimals: Optional[Union[int, str]] = None,
        scale: Union[int, str] = 0,
        sign: Optional[str] = None,
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

    def to_json(self):
        return deepcopy(self.__dict__)

    def parse_value(self, value: Union[str, int, float]) -> Optional[Union[int, float, bool, date]]:
        if isinstance(value, (int, float)):
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
