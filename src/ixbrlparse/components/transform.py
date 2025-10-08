from ixbrlparse.components._base import ixbrlFormat
from ixbrlparse.plugins import pm


def get_format(format_: str | None) -> type[ixbrlFormat]:
    if not isinstance(format_, str):
        return ixbrlFormat

    original_format: str = format_

    format_list: list[str] = format_.split(":")
    if len(format_list) > 1:
        namespace = format_list[0]
        format_ = ":".join(format_list[1:])
    else:
        namespace = None
        format_ = ":".join(format_list)

    format_ = format_.replace("-", "")

    formats = {}
    for additional_formats in pm.hook.ixbrl_add_formats():
        for format_class in additional_formats:
            for format_str in format_class.format_names:
                formats[format_str] = format_class

    if format_ in formats:
        return formats[format_]

    msg = f'Format "{original_format}" not implemented (namespace "{namespace}")'
    raise NotImplementedError(msg)
