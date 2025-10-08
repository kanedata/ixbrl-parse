import datetime
import re
import warnings
from collections.abc import Sequence

from word2number import w2n

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

    def parse_value(self, *_args, **_kwargs) -> int | float:
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

    def parse_value(self, value: str | int | float) -> int | float | None:
        if isinstance(value, str):
            value = value.replace(".", "")
            value = value.replace(",", ".")
        parsed_value = super().parse_value(value)
        if isinstance(parsed_value, float | int):
            return parsed_value
        msg = f"Could not parse value {value} as a number"  # pragma: no cover
        warnings.warn(msg, stacklevel=2)  # pragma: no cover
        return None  # pragma: no cover


class ixtNumWordsEn(ixbrlFormat):  # noqa: N801
    format_names = (
        "numwordsen",
        "ixt:numwordsen",
    )

    def parse_value(self, value: str | int | float) -> int | float | None:
        if isinstance(value, str):
            value = value.strip().lower()
            if value in ("no", "none"):
                return 0

            return w2n.word_to_num(value)
        parsed_value = super().parse_value(value)
        if isinstance(parsed_value, float | int):
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
DATE_NON_ALPHANUMERIC_REGEX = re.compile(r"[\/\.\-\\–— ]")  # noqa: RUF001


class ixtDateFormat(ixbrlFormat):  # noqa: N801
    format_names: tuple[str, ...] = ()
    date_format: tuple[str, ...] | str = "%Y-%m-%d"

    def _get_date_formats(self) -> Sequence[str]:
        if isinstance(self.date_format, str):
            return (self.date_format,)
        return self.date_format

    def parse_value(self, value: str | int | float) -> datetime.date | None:
        if isinstance(value, str):
            value = value.lower()
            # remove ordinal suffixes with regex
            value = DATE_ORDINAL_SUFFIX_REGEX.sub(r"\1", value)
            # replace non-alphanumeric characters with dashes
            value = DATE_NON_ALPHANUMERIC_REGEX.sub("-", value)

            date_formats = self._get_date_formats()
            error: Exception | None = None
            for date_format in date_formats:
                try:
                    return datetime.datetime.strptime(value, date_format).date()  # noqa: DTZ007
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
    date_format = ("%d-%B-%Y", "%d-%B-%y", "%d-%b-%Y", "%d-%b-%y")


class ixtDateShortUK(ixtDateFormat):  # noqa: N801
    format_names = (
        "dateshortuk",
        "ixt:dateshortuk",
    )
    date_format = ("%d-%b-%Y", "%d-%b-%y", "%d-%B-%Y", "%d-%B-%y")


class ixtDateLongUS(ixtDateFormat):  # noqa: N801
    format_names = (
        "datelongus",
        "ixt:datelongus",
    )
    date_format = ("%B-%d,-%Y", "%B-%d,-%y", "%b-%d,-%Y", "%b-%d,-%y")


class ixtDateShortUS(ixtDateFormat):  # noqa: N801
    format_names = (
        "dateshortus",
        "ixt:dateshortus",
    )
    date_format = ("%b-%d,-%Y", "%b-%d,-%y", "%B-%d,-%Y", "%B-%d,-%y")


class ixtDateDayMonthYear(ixtDateFormat):  # noqa: N801
    format_names = (
        "datedaymonthyear",
        "ixt:datedaymonthyear",
        "dateslasheu",
        "ixt:dateslasheu",
        "datedoteu",
        "ixt:datedoteu",
    )
    date_format = ("%d-%m-%Y", "%d-%m-%y")


class ixtDateSlashUS(ixtDateFormat):  # noqa: N801
    format_names = (
        "dateslashus",
        "ixt:dateslashus",
        "datedotus",
        "ixt:datedotus",
    )
    date_format = ("%m-%d-%Y", "%m-%d-%y")


class ixtDateDotEU(ixtDateDayMonthYear):  # noqa: N801
    pass


class ixtDateSlashEU(ixtDateDayMonthYear):  # noqa: N801
    pass


class ixtDateDotUS(ixtDateSlashUS):  # noqa: N801
    pass


@hookimpl(tryfirst=True)
def ixbrl_add_formats() -> list[type[ixbrlFormat]]:
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
        ixtDateSlashUS,
    ]
