import warnings
from copy import deepcopy
from datetime import date
from typing import Any

from bs4 import Tag

from ixbrlparse.components import ixbrlContext
from ixbrlparse.components.constants import NAME_SPLIT_EXPECTED
from ixbrlparse.components.transform import get_format, ixbrlFormat


class ixbrlNonNumeric:  # noqa: N801
    """Models a non-numeric element in an iXBRL document

    Non-numeric elements are used to store information such as the name of the
    entity, the name of the reporting period, etc.
    The value of non-numeric elements is always a string, so we don't need to
    worry about parsing the string."""

    def __init__(
        self,
        context: ixbrlContext | str | None = None,
        name: str | None = None,
        format_: str | None = None,
        value: str | None = None,
        soup_tag: Tag | None = None,
    ) -> None:
        """Constructor for the ixbrlNonNumeric class.

        Parameters:
            context (ixbrlContext): The context of the non-numeric element
            name (str): The name of the non-numeric element
            format_ (str): The format of the non-numeric element
            value (str): The value of the non-numeric element
            soup_tag (Tag): The source tag in beautiful soup
        """
        if isinstance(name, str):
            name_split: list[str] = name.split(":", maxsplit=1)
            if len(name_split) == NAME_SPLIT_EXPECTED:
                self.schema = name_split[0]
                self.name = name_split[1]
            else:
                self.schema = "unknown"
                self.name = name_split[0]

        self.context = context
        self.format: ixbrlFormat | None = None
        self.text: str | None = value
        self.value: str | int | float | None | date | None = value
        if isinstance(format_, str) and format_ != "" and self.text is not None:
            try:
                self.format = get_format(format_)(format_=format_)
                self.value = self.format.parse_value(self.text)
            except NotImplementedError:
                msg = f"Format {format_} not implemented - value '{value}' not parsed"
                warnings.warn(msg, stacklevel=2)
        self.soup_tag = soup_tag

    def to_json(self) -> dict[str, Any]:
        values = {k: deepcopy(v) for k, v in self.__dict__.items() if k != "soup_tag"}
        if isinstance(self.value, date):
            values["value"] = self.value.isoformat()
        if isinstance(self.format, ixbrlFormat):
            values["format"] = self.format.to_json()
        if isinstance(self.context, ixbrlContext):
            values["context"] = self.context.to_json()
        return values
