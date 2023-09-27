import datetime
import re
import warnings
from typing import List, Optional, Sequence, Tuple, Type, Union

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
    date_format: Union[Tuple[str, ...], str] = "%Y-%m-%d"

    def _get_date_formats(self) -> Sequence[str]:
        if isinstance(self.date_format, str):
            return (self.date_format,)
        return self.date_format

    def parse_value(self, value: Union[str, int, float]) -> Optional[datetime.date]:
        if isinstance(value, str):
            value = value.lower()
            # remove ordinal suffixes with regex
            value = DATE_ORDINAL_SUFFIX_REGEX.sub(r"\1", value)
            date_formats = self._get_date_formats()
            error: Optional[Exception] = None
            for date_format in date_formats:
                try:
                    return datetime.datetime.strptime(value, date_format).astimezone().date()
                except ValueError as e:
                    error = e
                    continue
            # if we get here, we couldn't parse the date. Raise the last error
            if error:  # pragma: no cover
                raise error
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
    date_format = ("%d %B %Y", "%d %B %y")


class ixtDateLongUS(ixtDateFormat):  # noqa: N801
    format_names = (
        "datelongus",
        "ixt:datelongus",
    )
    date_format = ("%B %d, %Y", "%B %d, %y")


class ixtDateShortUK(ixtDateFormat):  # noqa: N801
    format_names = (
        "dateshortuk",
        "ixt:dateshortuk",
    )
    date_format = ("%d %b %Y", "%d %b %y")


class ixtDateShortUS(ixtDateFormat):  # noqa: N801
    format_names = (
        "dateshortus",
        "ixt:dateshortus",
    )
    date_format = ("%b %d, %Y", "%b %d, %y")


class ixtDateDayMonthYear(ixtDateFormat):  # noqa: N801
    format_names = (
        "datedaymonthyear",
        "ixt:datedaymonthyear",
    )
    date_format = ("%d.%m.%Y", "%d.%m.%y")


class ixtDateSlashEU(ixtDateFormat):  # noqa: N801
    format_names = (
        "dateslasheu",
        "ixt:dateslasheu",
    )
    date_format = ("%d/%m/%Y", "%d/%m/%y")


class ixtDateSlashUS(ixtDateFormat):  # noqa: N801
    format_names = (
        "dateslashus",
        "ixt:dateslashus",
    )
    date_format = ("%m/%d/%Y", "%m/%d/%y")


class ixtDateDotEU(ixtDateFormat):  # noqa: N801
    format_names = (
        "datedoteu",
        "ixt:datedoteu",
    )
    date_format = ("%d.%m.%y", "%d.%m.%Y")


class ixtDateDotUS(ixtDateFormat):  # noqa: N801
    format_names = (
        "datedotus",
        "ixt:datedotus",
    )
    date_format = ("%m.%d.%y", "%m.%d.%Y")


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
        ixtDateLongUS,
        ixtDateShortUK,
        ixtDateShortUS,
        ixtDateDayMonthYear,
        ixtDateSlashEU,
        ixtDateSlashUS,
        ixtDateDotEU,
        ixtDateDotUS,
    ]
