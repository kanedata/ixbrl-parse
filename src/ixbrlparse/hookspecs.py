from typing import List, Type

import pluggy

from ixbrlparse.components.transform import ixbrlFormat

hookimpl = pluggy.HookimplMarker("ixbrlparse")
hookspec = pluggy.HookspecMarker("ixbrlparse")


@hookspec
def ixbrl_add_formats() -> List[Type[ixbrlFormat]]:  # type: ignore
    """Add new formats to the ixbrlparse library.

    Returns:
        List[[ixbrlFormat]]: A list of ixbrlFormat classes.
    """
