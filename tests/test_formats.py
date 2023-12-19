from datetime import date

import pytest

from ixbrlparse.components.formats import (
    ixbrlFormat,
    ixtDateDayMonthYear,
    ixtDateFormat,
    ixtDateLongUK,
    ixtDateLongUS,
    ixtDateShortUK,
    ixtDateShortUS,
    ixtDateSlashUS,
    ixtFixedFalse,
    ixtFixedTrue,
    ixtNoContent,
    ixtNumComma,
    ixtNumDotDecimal,
    ixtNumWordsEn,
    ixtZeroDash,
)


@pytest.mark.parametrize(
    "dateclass, datestring, expecteddate, errordate",
    (
        (ixtDateFormat, "2019-01-05", date(2019, 1, 5), "0400502019"),
        (ixtDateLongUK, "05 January 2019", date(2019, 1, 5), "0400502019"),
        (ixtDateLongUK, "05 January 19", date(2019, 1, 5), "0400502019"),
        (ixtDateLongUS, "January 05, 2019", date(2019, 1, 5), "0400502019"),
        (ixtDateLongUS, "January 05, 19", date(2019, 1, 5), "0400502019"),
        (ixtDateShortUK, "05 Jan 2019", date(2019, 1, 5), "0400502019"),
        (ixtDateShortUK, "05 Jan 19", date(2019, 1, 5), "0400502019"),
        (ixtDateShortUS, "Jan 05, 2019", date(2019, 1, 5), "0400502019"),
        (ixtDateShortUS, "Jan 05, 19", date(2019, 1, 5), "0400502019"),
        (ixtDateDayMonthYear, "05/01/2019", date(2019, 1, 5), "0400502019"),
        (ixtDateDayMonthYear, "05.01.2019", date(2019, 1, 5), "0400502019"),
        (ixtDateDayMonthYear, "05.01.19", date(2019, 1, 5), "0400502019"),
        (ixtDateDayMonthYear, "05/01/2019", date(2019, 1, 5), "2019005004"),
        (ixtDateDayMonthYear, "05/01/19", date(2019, 1, 5), "2019005004"),
        (ixtDateSlashUS, "01/05/2019", date(2019, 1, 5), "2019005004"),
        (ixtDateSlashUS, "01/05/19", date(2019, 1, 5), "2019005004"),
        (ixtDateDayMonthYear, "05.01.2019", date(2019, 1, 5), "0400502019"),
        (ixtDateDayMonthYear, "05.01.19", date(2019, 1, 5), "0400502019"),
        (ixtDateSlashUS, "01.05.2019", date(2019, 1, 5), "0400502019"),
        (ixtDateSlashUS, "01.05.19", date(2019, 1, 5), "0400502019"),
    ),
)
def test_date_formats(dateclass, datestring, expecteddate, errordate):
    f = dateclass("dateformat")
    assert f.parse_value(datestring) == expecteddate

    with pytest.warns():
        assert f.parse_value(1234) is None

    with pytest.raises(ValueError):
        assert f.parse_value(errordate) is None


def test_ixtnumwordsen():
    f = ixtNumWordsEn("format")
    assert f.parse_value("no") == 0
    assert f.parse_value("eighty-five") == 85.0

    with pytest.raises(ValueError):
        assert f.parse_value("blurdy-burg") is None


def test_ixtnumcomma():
    f = ixtNumComma("format")
    assert f.parse_value("0") == 0
    assert f.parse_value("85") == 85.0
    assert f.parse_value("85.123") == 85123.0

    with pytest.raises(ValueError):
        assert f.parse_value("blurdy-burg") is None


@pytest.mark.parametrize(
    "formatclass, valuestring, expectedvalue, errorvalue",
    (
        (ixbrlFormat, None, None, None),
        (ixtFixedFalse, "hfkjdah", False, None),
        (ixtFixedTrue, "hfkjdah", True, None),
        (ixtNoContent, "hfkjdah", None, None),
        (ixtNumDotDecimal, "235,100,356.79", 235_100_356.79, None),
        (ixtNumDotDecimal, "100,356.79", 100_356.79, None),
        (ixtNumDotDecimal, "100", 100, None),
        (ixtNumDotDecimal, 100, 100, None),
        (ixtNumComma, "235.100.345,79", 235_100_345.79, None),
        (ixtNumComma, "100.345,79", 100_345.79, None),
        (ixtNumComma, "100", 100, None),
        (ixtNumComma, 100, 100, None),
        (ixtZeroDash, "cjsjdsf", 0, None),
        (ixtZeroDash, "-", 0, None),
    ),
)
def test_formats(formatclass, valuestring, expectedvalue, errorvalue):
    f = formatclass("format")
    assert f.parse_value(valuestring) == expectedvalue

    if errorvalue is not None:
        with pytest.raises(ValueError):
            assert f.parse_value(errorvalue) is None
