import datetime
import re
import warnings
from typing import List, Optional, Tuple, Type, Union

from ixbrlparse.components._base import ixbrlFormat
from ixbrlparse.hookspecs import hookimpl


class ixtZeroDash(ixbrlFormat):  # noqa: N801
    format_names = (
        "zerodash",
        "numdash",
        "fixedzero",
        "ixt:zerodash",
        "ixt:numdash",
        "ixt:fixedzero",
    )

    def parse_value(self, *_args, **_kwargs) -> Union[int, float]:
        return 0


class ixtNoContent(ixbrlFormat):  # noqa: N801
    format_names = (
        "nocontent",
        "fixedempty",
        "ixt:nocontent",
        "ixt:fixedempty",
    )

    def parse_value(self, *_args, **_kwargs) -> None:
        return None


class ixtFixedFalse(ixbrlFormat):  # noqa: N801
    format_names = (
        "booleanfalse",
        "fixedfalse",
        "ixt:booleanfalse",
        "ixt:fixedfalse",
    )

    def parse_value(self, *_args, **_kwargs) -> bool:
        return False


class ixtFixedTrue(ixbrlFormat):  # noqa: N801
    format_names = (
        "booleantrue",
        "fixedtrue",
        "ixt:booleantrue",
        "ixt:fixedtrue",
    )

    def parse_value(self, *_args, **_kwargs) -> bool:
        return True


class ixtNumComma(ixbrlFormat):  # noqa: N801
    format_names = (
        "numcomma",
        "numdotcomma",
        "numspacecomma",
        "numcommadecimal",
        "ixt:numcomma",
        "ixt:numdotcomma",
        "ixt:numspacecomma",
        "ixt:numcommadecimal",
    )

    def parse_value(self, value: Union[str, int, float]) -> Optional[Union[int, float]]:
        if isinstance(value, str):
            value = value.replace(".", "")
            value = value.replace(",", ".")
        parsed_value = super().parse_value(value)
        if isinstance(parsed_value, (float, int)):
            return parsed_value
        msg = f"Could not parse value {value} as a number"  # pragma: no cover
        warnings.warn(msg, stacklevel=2)  # pragma: no cover
        return None  # pragma: no cover


class ixtNumWordsEn(ixbrlFormat):  # noqa: N801
    format_names = (
        "numwordsen",
        "ixt:numwordsen",
    )

    def parse_value(self, value: Union[str, int, float]) -> Optional[Union[int, float]]:
        if isinstance(value, str):
            value = value.lower()
            if value in ("no", "none"):
                return 0
            from word2number import w2n

            return w2n.word_to_num(value)
        parsed_value = super().parse_value(value)
        if isinstance(parsed_value, (float, int)):
            return parsed_value
        msg = f"Could not parse value {value} as a number"  # pragma: no cover
        warnings.warn(msg, stacklevel=2)  # pragma: no cover
        return None  # pragma: no cover


class ixtNumDotDecimal(ixbrlFormat):  # noqa: N801
    format_names = (
        "numdotdecimal",
        "numcommadot",
        "numspacedot",
        "ixt:numdotdecimal",
        "ixt:numcommadot",
        "ixt:numspacedot",
    )


DATE_ORDINAL_SUFFIX_REGEX = re.compile(r"([0-9]{1,2})(st|nd|rd|th)\b")


class ixtDateFormat(ixbrlFormat):  # noqa: N801
    format_names: Tuple[str, ...] = ()
    date_format = "%Y-%m-%d"

    def parse_value(self, value: Union[str, int, float]) -> Optional[datetime.date]:
        if isinstance(value, str):
            value = value.lower()
            # remove ordinal suffixes with regex
            value = DATE_ORDINAL_SUFFIX_REGEX.sub(r"\1", value)
            return datetime.datetime.strptime(value, self.date_format).astimezone().date()
        msg = f"Could not parse value {value} as a date"
        warnings.warn(msg, stacklevel=2)
        return None


class ixtDateLongUK(ixtDateFormat):  # noqa: N801
    format_names = (
        "datelonguk",
        "datedaymonthyearen",
        "ixt:datelonguk",
        "ixt:datedaymonthyearen",
    )
    date_format = "%d %B %Y"


class ixtDateDayMonthYear(ixtDateFormat):  # noqa: N801
    format_names = (
        "datedaymonthyear",
        "ixt:datedaymonthyear",
    )
    date_format = "%d.%m.%y"


@hookimpl
def ixbrl_add_formats() -> List[Type[ixbrlFormat]]:
    return [
        ixtZeroDash,
        ixtNoContent,
        ixtFixedFalse,
        ixtFixedTrue,
        ixtNumDotDecimal,
        ixtNumComma,
        ixtNumWordsEn,
        ixtDateLongUK,
        ixtDateDayMonthYear,
    ]
