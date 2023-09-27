from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Tuple, Union

from bs4 import Tag


@dataclass
class ixbrlError:  # noqa: N801
    error: Exception
    element: Optional[Tag] = None
    context: Optional[str] = None


class ixbrlFormat:  # noqa: N801
    """Class to represent an ixbrl format.

    This class should generally be subclassed to provide additional functionality.

    Attributes:
        format_names: A tuple of format names that this class should be used for."""

    format_names: Tuple[str, ...] = ()

    def __init__(
        self,
        format_: str,
        decimals: Optional[Union[int, str]] = None,
        scale: Union[int, str] = 0,
        sign: Optional[str] = None,
    ) -> None:
        """Initialise the ixbrl format object.

        Parameters:
            format_: The name of the format.
            decimals: The number of decimal places (only used for numeric formats).
            scale: The scale of the format (only for numeric formats).
                If more than 0 this value is used as the exponent for a value, so for example with a scale of
                4 and a value of 20, the parsed value is 20 * (10 ^ 4) == 200000.
            sign: The sign of the format (only for numeric formats). The sign given is usually "-" or empty.
        """
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
        """Convert the object to a JSON serialisable dictionary."""
        return deepcopy(self.__dict__)

    def parse_value(self, value: Union[str, int, float]) -> Optional[Union[int, float, bool, date, str]]:
        """Parse a value using the format.

        Parameters:
            value: The value to parse.

        Returns:
            The parsed value in the appropriate python type.
        """
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
