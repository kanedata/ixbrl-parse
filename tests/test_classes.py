import datetime
import pytest

from ixbrlparse.core import ixbrlContext, ixbrlNonNumeric, ixbrlNumeric


def test_context():

    instant_context = ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": None,
        "instant": "2011-01-01",
        "startdate": None,
        "enddate": None,
    })
    assert isinstance(instant_context.instant, datetime.date)
    assert "2011-01-01" in str(instant_context)

    interval = ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": None,
        "instant": None,
        "startdate": "2011-01-01",
        "enddate": "2011-12-31",
    })
    assert isinstance(interval.startdate, datetime.date)
    assert isinstance(interval.enddate, datetime.date)
    assert interval.startdate.year == 2011
    assert interval.enddate.month == 12

    # @TODO: Validation of values - eg startdate before enddate


def test_context_json():

    instant_context = ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": None,
        "instant": "2011-01-01",
        "startdate": None,
        "enddate": None,
    }).to_json()
    assert instant_context["instant"] == "2011-01-01"
    assert instant_context["startdate"] is None

    interval = ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": None,
        "instant": None,
        "startdate": "2011-01-01",
        "enddate": "2011-12-31",
    }).to_json()
    assert interval["startdate"] == "2011-01-01"
    assert interval["instant"] is None


def test_context_segments():

    i = ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": [{
            "tag": "1",
            "value": "2",
            "dimension": "3"
        }],
        "instant": None,
        "startdate": "2011-01-01",
        "enddate": "2011-12-31",
    })
    assert len(i.segments) == 1
    assert i.segments[0]["value"] == "2"
    assert "with segment" in str(i)


def test_nonnumeric():

    a = {"context": {}, "format_": "", "value": ""}

    x = ixbrlNonNumeric(name="value", **a)
    assert x.schema == "unknown"
    assert x.name == "value"


def test_nonnumeric_json():

    a = {"context": ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": None,
        "instant": "2011-01-01",
        "startdate": None,
        "enddate": None,
    }), "format_": "", "value": ""}

    x = ixbrlNonNumeric(name="value", **a).to_json()
    assert "context" in x


def test_nonnumeric_schema():

    a = {"context": "", "format_": "", "value": ""}

    x = ixbrlNonNumeric(name="schema:value", **a)
    assert x.schema == "schema"
    assert x.name == "value"


def test_numeric_value():

    assert ixbrlNumeric({"text": "1234"}).value == 1234
    assert ixbrlNumeric({"value": "1234"}).value == 1234


def test_numeric_value_error():

    with pytest.raises(ValueError):
        ixbrlNumeric({"text": "1234blahblab"})
    with pytest.raises(ValueError):
        ixbrlNumeric({"value": "1234blahblah"})


def test_numeric_to_json():

    assert ixbrlNumeric({"context": ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": None,
        "instant": "2011-01-01",
        "startdate": None,
        "enddate": None,
    }), "text": "1234"}).to_json()["value"] == 1234
    assert ixbrlNumeric({"context": ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": None,
        "instant": "2011-01-01",
        "startdate": None,
        "enddate": None,
    }), "value": "1234"}).to_json()["value"] == 1234


def test_numeric_already_float():

    assert ixbrlNumeric({"value": 1234}).value == 1234
    assert ixbrlNumeric({"value": 1234.0}).value == 1234


def test_numeric_comma_replace():

    assert ixbrlNumeric({"text": "1,234"}).value == 1234
    assert ixbrlNumeric({"value": "1,234"}).value == 1234


def test_numeric_sign():

    assert ixbrlNumeric({"text": "1,234", "sign": "-"}).value == -1234
    assert ixbrlNumeric({"value": "1,234", "sign": "-"}).value == -1234
    assert ixbrlNumeric({"value": "1,234", "sign": ""}).value == 1234


def test_numeric_blank():

    assert ixbrlNumeric({"value": "-"}).value == 0
    assert ixbrlNumeric({"text": "-"}).value == 0


def test_numeric_scale():

    assert ixbrlNumeric({"value": "1,234", "scale": "0"}).value == 1234
    assert ixbrlNumeric({"value": "1,234", "scale": "1"}).value == 12340
    assert ixbrlNumeric({"text": "1,234", "scale": "2"}).value == 123400


def test_numeric_scale_sign():

    assert ixbrlNumeric({"value": "1,234", "scale": "3", "sign": "-"}).value == -1234000
    assert ixbrlNumeric({"text": "1,234", "scale": "3", "sign": "-"}).value == -1234000


def test_numeric_inf_format():

    assert ixbrlNumeric({"text": "1234", "decimals": "INF"}).value == 1234


def test_format_zerodash():

    assert ixbrlNumeric({"text": "-", "format": "zerodash"}).value == 0
    assert ixbrlNumeric({"text": "-", "format": "numdash"}).value == 0
    assert ixbrlNumeric({"text": "-", "format": "numdotdecimal"}).value == 0


def test_format_nocontent():

    assert ixbrlNumeric({"text": "-", "format": "nocontent"}).value == 0


def test_format_numdotdecimal():

    assert ixbrlNumeric({"text": "1234.12", "format": "numdotdecimal"}).value == 1234.12
    assert ixbrlNumeric({"text": "1234", "format": "numdotdecimal"}).value == 1234
    assert ixbrlNumeric({"text": "1234.34", "format": "numcommadot"}).value == 1234.34
    assert ixbrlNumeric({"text": "1234.45", "format": "numspacedot"}).value == 1234.45
    assert ixbrlNumeric({"text": "1,234.45", "format": "numspacedot"}).value == 1234.45
    assert ixbrlNumeric({"text": "1234.12", "format": "num-dot-decimal"}).value == 1234.12


def test_format_numcomma():

    assert ixbrlNumeric({"text": "1234,12", "format": "numcomma"}).value == 1234.12
    assert ixbrlNumeric({"text": "1234", "format": "numcomma"}).value == 1234
    assert ixbrlNumeric({"text": "1234,34", "format": "numcomma"}).value == 1234.34
    assert ixbrlNumeric({"text": "1234,45", "format": "numcomma"}).value == 1234.45
    assert ixbrlNumeric({"text": "1.234,45", "format": "numcomma"}).value == 1234.45
    assert ixbrlNumeric({"text": "1234,12", "format": "numcomma"}).value == 1234.12


def test_format_numwordsen():

    assert ixbrlNumeric({"text": "one thousand two hundred and thirty four", "format": "numwordsen"}).value == 1234
    assert ixbrlNumeric({"text": "eight", "format": "numwordsen"}).value == 8
    assert ixbrlNumeric({"text": "one thousand two hundred and thirty four point four five", "format": "numwordsen"}).value == 1234.45
