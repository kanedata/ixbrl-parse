from datetime import date
from bs4 import BeautifulSoup
from ixbrlparse import IXBRL
from ixbrlparse.core import ixbrlContext, ixbrlNonNumeric, ixbrlNumeric

TEST_ACCOUNTS = [
    "tests/test_accounts/account_1.html",
    "tests/test_accounts/account_2.html",
    "tests/test_accounts/account_3.html",
    "tests/test_accounts/account_4.html",
]

def test_open():
    with open(TEST_ACCOUNTS[0]) as a:
        x = IXBRL(a)
        assert isinstance(x.soup, BeautifulSoup)

    x = IXBRL.open(TEST_ACCOUNTS[1])
    assert isinstance(x.soup, BeautifulSoup)

def test_schema():
    account_schema = [
        ("https://xbrl.frc.org.uk/FRS-102/2014-09-01/FRS-102-2014-09-01.xsd", 11),
        ("http://www.xbrl.org/uk/gaap/core/2009-09-01/uk-gaap-full-2009-09-01.xsd", 12),
        ("http://www.xbrl.org/uk/gaap/core/2009-09-01/uk-gaap-full-2009-09-01.xsd", 12),
        ("https://xbrl.frc.org.uk/FRS-102/2014-09-01/FRS-102-2014-09-01.xsd", 38),
    ]

    for k, a in enumerate(TEST_ACCOUNTS):
        x = IXBRL.open(a)
        assert x.schema == account_schema[k][0]
        assert len(x.namespaces) == account_schema[k][1]

def test_contexts():
    x = IXBRL.open(TEST_ACCOUNTS[0])

    # test all the contexts have been found
    assert len(x.contexts) == 12

    # test that the context is correct class
    assert isinstance(list(x.contexts.values())[0], ixbrlContext)

    # test an expected key is in the contexts
    assert "dcur6" in x.contexts

    # test values have been correctly parsed
    assert x.contexts["icur1"].instant == date(2017, 10, 31)
    assert x.contexts["dcur1"].startdate == date(2016, 11, 1)
    assert x.contexts["dcur1"].enddate == date(2017, 10, 31)
    assert x.contexts["dcur1"].entity == "05969206"

    # @TODO: I think a context can have multiple dimensions/segments
    assert x.contexts["dcur1"].dimension == "uk-bus:EntityOfficersDimension"
    assert x.contexts["dcur1"].segment == "uk-bus:Director1"

def test_units():
    x = IXBRL.open(TEST_ACCOUNTS[1])

    assert len(x.units) == 2
    assert x.units["currencyUnit"] == "iso4217:GBP"

def test_nonnumeric():
    x = IXBRL.open(TEST_ACCOUNTS[2])

    assert len(x.nonnumeric) == 15
    assert isinstance(x.nonnumeric[0], ixbrlNonNumeric)
    assert "SAKO TECHNOLOGIES LIMITED" in [n.value for n in x.nonnumeric]
    for n in x.nonnumeric:
        if n.schema == "uk-gaap-cd-bus" and n.name == "UKCompaniesHouseRegisteredNumber":
            assert n.value == "07713141"
            assert isinstance(n.context, ixbrlContext)

def test_numeric():
    x = IXBRL.open(TEST_ACCOUNTS[3])

    assert len(x.numeric) == 32
    for n in x.numeric:
        assert isinstance(n, ixbrlNumeric)

        if n.name == "NetCurrentAssetsLiabilities" and n.context._id == "cfwd_31_03_2017":
            assert n.format["sign"] == "-"
            assert n.value == -17957

        if n.format["sign"] == "-":
            assert n.value < 0

    assert x.numeric[0].unit == "iso4217:GBP"
    assert x.numeric[0].value == 52982
    assert x.numeric[0].name == "PropertyPlantEquipment"
    assert x.numeric[0].schema == "ns5"
