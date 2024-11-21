import pluggy

from ixbrlparse.components.transform import ixbrlFormat

hookimpl = pluggy.HookimplMarker("ixbrlparse")
hookspec = pluggy.HookspecMarker("ixbrlparse")


@hookspec
def ixbrl_add_formats() -> list[type[ixbrlFormat]]:  # type: ignore
    """Add new formats to the ixbrlparse library.

    Returns:
        list[[ixbrlFormat]]: A list of ixbrlFormat classes.
    """
