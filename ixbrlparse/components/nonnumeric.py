from copy import deepcopy
from typing import Optional, Any, Union

from ixbrlparse.components import ixbrlContext


class ixbrlNonNumeric:
    def __init__(
        self,
        context: Union[ixbrlContext, str, None],
        name: str,
        format_: Optional[str],
        value: str,
    ) -> None:

        name_split: list[str] = name.split(":", maxsplit=1)
        if len(name_split) == 2:
            self.schema = name_split[0]
            self.name = name_split[1]
        else:
            self.schema = "unknown"
            self.name = name_split[0]

        self.context = context
        self.format = format_
        self.value = value

    def to_json(self) -> dict[str, Any]:
        values = deepcopy(self.__dict__)
        if isinstance(self.context, ixbrlContext):
            values["context"] = self.context.to_json()
        return values
