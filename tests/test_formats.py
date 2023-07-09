from datetime import date

import pytest

from ixbrlparse.components.formats import ixtDateFormat, ixtNumComma, ixtNumWordsEn


def test_ixbrl_date_format():
    f = ixtDateFormat("dateformat")
    assert f.parse_value("2019-01-01") == date(2019, 1, 1)

    with pytest.warns():
        assert f.parse_value(1234) is None

    with pytest.raises(ValueError):
        assert f.parse_value("04/05/2019") is None


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
