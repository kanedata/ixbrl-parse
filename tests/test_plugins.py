from datetime import date
from typing import Union

import pytest

from ixbrlparse import hookimpl
from ixbrlparse.components._base import ixbrlFormat
from ixbrlparse.components.formats import ixtDateDayMonthYear, ixtZeroDash
from ixbrlparse.components.transform import get_format
from ixbrlparse.plugins import pm


def test_using_test_plugin():
    class FlurgFormat(ixbrlFormat):
        format_names = ("flurg",)

        def parse_value(self, value: Union[str, int, float]) -> str:  # noqa: ARG002
            return "flurg"

    class TestPlugin:
        @hookimpl
        def ixbrl_add_formats(self) -> list[type[ixbrlFormat]]:
            return [FlurgFormat]

    pm.register(TestPlugin(), name="flurg")
    try:
        # check new format is available
        assert get_format("flurg") == FlurgFormat

        # check existing formats are still available
        assert get_format("zerodash") == ixtZeroDash
    finally:
        pm.unregister(name="flurg")


def test_using_test_plugin_alt_syntax():
    class FlurgFormat(ixbrlFormat):
        format_names = ("flurg",)

        def parse_value(self, value: Union[str, int, float]) -> str:  # noqa: ARG002
            return "flurg"

    class TestPlugin:
        @hookimpl(specname="ixbrl_add_formats")
        def add_flurg_format(self) -> list[type[ixbrlFormat]]:
            return [FlurgFormat]

    pm.register(TestPlugin(), name="flurg")
    try:
        # check new format is available
        assert get_format("flurg") == FlurgFormat

        # check existing formats are still available
        assert get_format("zerodash") == ixtZeroDash
    finally:
        pm.unregister(name="flurg")


def test_registering_duplicate_plugin():
    class FlurgFormat(ixbrlFormat):
        format_names = ("zerodash",)

        def parse_value(self, value: Union[str, int, float]) -> str:  # noqa: ARG002
            return "flurg"

    class TestPlugin:
        @hookimpl()
        def ixbrl_add_formats(self) -> list[type[ixbrlFormat]]:
            return [FlurgFormat]

    pm.register(TestPlugin(), name="flurg")
    try:
        assert get_format("zerodash") == FlurgFormat
        with pytest.raises(NotImplementedError):
            get_format("flurg")
    finally:
        pm.unregister(name="flurg")


def test_registering_duplicate_plugin_last():
    class FlurgFormat(ixbrlFormat):
        format_names = ("zerodash",)

        def parse_value(self, value: Union[str, int, float]) -> str:  # noqa: ARG002
            return "flurg"

    class TestPlugin:
        @hookimpl(trylast=True)
        def ixbrl_add_formats(self) -> list[type[ixbrlFormat]]:
            return [FlurgFormat]

    pm.register(TestPlugin(), name="flurg")
    try:
        assert get_format("zerodash") == FlurgFormat
        with pytest.raises(NotImplementedError):
            get_format("flurg")
    finally:
        pm.unregister(name="flurg")


def test_registering_duplicate_plugin_first():
    class FlurgFormat(ixbrlFormat):
        format_names = ("zerodash",)

        def parse_value(self, value: Union[str, int, float]) -> str:  # noqa: ARG002
            return "flurg"

    class TestPlugin:
        @hookimpl(tryfirst=True)
        def ixbrl_add_formats(self) -> list[type[ixbrlFormat]]:
            return [FlurgFormat]

    pm.register(TestPlugin(), name="flurg")
    try:
        assert get_format("zerodash") == ixtZeroDash
        with pytest.raises(NotImplementedError):
            get_format("flurg")
    finally:
        pm.unregister(name="flurg")


@pytest.mark.parametrize(
    "datestring, expecteddate",
    (
        ("05/01/2019", date(2019, 1, 5)),
        ("05.01.2019", date(2019, 1, 5)),
        ("05.01.19", date(2019, 1, 5)),
        ("05/01/2019", date(2019, 1, 5)),
        ("05/01/19", date(2019, 1, 5)),
        ("05.01.2019", date(2019, 1, 5)),
        ("05.01.19", date(2019, 1, 5)),
        ("29 aug 2022", date(2022, 8, 29)),
    ),
)
def test_plugin_override_date(datestring, expecteddate):
    class FlurgFormat(ixtDateDayMonthYear):
        date_format = (*ixtDateDayMonthYear.date_format, "%d-%b-%Y", "%d-%b-%y")

    class TestPlugin:
        @hookimpl
        def ixbrl_add_formats(self) -> list[type[ixbrlFormat]]:
            return [FlurgFormat]

    pm.register(TestPlugin(), name="flurg")
    format_class = get_format("datedaymonthyear")
    try:
        assert format_class == FlurgFormat
        assert format_class("datedaymonthyear").parse_value(datestring) == expecteddate
    finally:
        pm.unregister(name="flurg")
