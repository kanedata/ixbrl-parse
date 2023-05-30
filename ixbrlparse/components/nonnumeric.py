from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

from bs4 import Tag

from ixbrlparse.components import ixbrlContext


class ixbrlNonNumeric:
    def __init__(
        self,
        context: Union[ixbrlContext, str, None],
        name: str,
        format_: Optional[str],
        value: str,
        soup_tag: Optional[Tag] = None,
    ) -> None:
        name_split: List[str] = name.split(":", maxsplit=1)
        if len(name_split) == 2:
            self.schema = name_split[0]
            self.name = name_split[1]
        else:
            self.schema = "unknown"
            self.name = name_split[0]

        self.context = context
        self.format = format_
        self.value = value
        self.soup_tag = soup_tag

    def to_json(self) -> Dict[str, Any]:
        values = {k: deepcopy(v) for k, v in self.__dict__.items() if k != "soup_tag"}
        if isinstance(self.context, ixbrlContext):
            values["context"] = self.context.to_json()
        return values
