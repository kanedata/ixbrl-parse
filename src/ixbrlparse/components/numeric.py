import logging
from copy import deepcopy

from bs4 import Tag

from ixbrlparse.components.constants import NAME_SPLIT_EXPECTED
from ixbrlparse.components.context import ixbrlContext
from ixbrlparse.components.transform import get_format, ixbrlFormat


class ixbrlNumeric:  # noqa: N801
    """Models a numeric element in an iXBRL document"""

    def __init__(
        self,
        name: str | None = None,
        unit: str | None = None,
        value: str | int | float | None = None,
        text: str | int | float | None = None,
        context: ixbrlContext | str | None = None,
        soup_tag: Tag | None = None,
        **attrs,
    ) -> None:
        """Constructor for the ixbrlNumeric class.

        Parameters:
            name (str): The name of the numeric element
            unit (str): The unit of the numeric element
            value (float): The value of the numeric element
            text (str): The text of the numeric element
            context (ixbrlContext): The context of the numeric element
            soup_tag (Tag): The source tag in beautiful soup
        """
        self.name: str | None = name
        self.schema: str = "unknown"
        if isinstance(name, str):
            name_value = name.split(":", maxsplit=1)
            if len(name_value) == NAME_SPLIT_EXPECTED:
                self.schema = name_value[0]
                self.name = name_value[1]
            else:
                self.schema = "unknown"
                self.name = name_value[0]

        if not isinstance(value, str | int | float):
            value = text
        if not isinstance(value, str | int | float):
            msg = "Must provide either value or text"
            raise ValueError(msg)
        self.text: str | int | float = value
        self.context: ixbrlContext | str | None = context
        self.unit: str | None = unit
        self.value: int | float | None = None
        self.soup_tag = soup_tag

        format_ = {
            "format_": attrs.get("format"),
            "decimals": attrs.get("decimals", "0"),
            "scale": attrs.get("scale", 0),
            "sign": attrs.get("sign", ""),
        }
        self.format: ixbrlFormat | None = get_format(format_["format_"])(**format_)

        try:
            if isinstance(self.format, ixbrlFormat):
                parsed_value = self.format.parse_value(self.text)
                if isinstance(parsed_value, int | float):
                    self.value = parsed_value
        except ValueError:
            logging.info(attrs)
            raise

    def to_json(self) -> dict:
        values = {k: deepcopy(v) for k, v in self.__dict__.items() if k != "soup_tag"}
        if isinstance(self.format, ixbrlFormat):
            values["format"] = self.format.to_json()
        if isinstance(self.context, ixbrlContext):
            values["context"] = self.context.to_json()
        return values
