import datetime
from ixbrlparse.core import ixbrlContext, ixbrlNonNumeric, ixbrlNumeric

def test_context():

    assert isinstance(ixbrlContext(**{
        "_id": "123456",
        "entity": None,
        "segments": None,
        "instant": "2011-01-01",
        "startdate": None,
        "enddate": None,
    }).instant, datetime.date)

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

    a = {"context": "", "format_": "", "value": ""}

    x = ixbrlNonNumeric(name="value", **a)
    assert x.schema == "unknown"
    assert x.name == "value"

def test_nonnumeric_schema():

    a = {"context": "", "format_": "", "value": ""}

    x = ixbrlNonNumeric(name="schema:value", **a)
    assert x.schema == "schema"
    assert x.name == "value"

def test_numeric_value():

    assert ixbrlNumeric({"text": "1234"}).value == 1234
    assert ixbrlNumeric({"value": "1234"}).value == 1234

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
