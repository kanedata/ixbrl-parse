from collections.abc import Generator, Iterable
from pathlib import Path
from typing import IO

from bs4 import BeautifulSoup, Tag

from ixbrlparse.components import ixbrlContext, ixbrlNonNumeric, ixbrlNumeric
from ixbrlparse.components._base import ixbrlError

FILETYPE_IXBRL = "ixbrl"
FILETYPE_XBRL = "xbrl"


class IXBRLParseError(Exception):
    pass


class BaseParser:
    def _get_tag_attribute(self, s: BeautifulSoup | Tag, tag: str | list[str], attribute: str) -> str | None:
        tag_contents = s.find(tag)
        if isinstance(tag_contents, Tag):
            attribute_value = tag_contents.get(attribute)
            if isinstance(attribute_value, str):
                return attribute_value.strip()
        return None  # pragma: no cover

    def _get_tag_text(self, s: BeautifulSoup | Tag, tag: str | list[str]) -> str | None:
        tag_contents = s.find(tag)
        if isinstance(tag_contents, Tag):
            text_value = tag_contents.text
            if isinstance(text_value, str):
                return text_value.strip()
        return None  # pragma: no cover

    def _get_tag_children(self, s: BeautifulSoup | Tag, tag: str | list[str]) -> Iterable[Tag]:
        tag_contents = s.find(tag)
        if isinstance(tag_contents, Tag):
            return tag_contents.findChildren()
        return []

    def _get_schema(self) -> None:
        pass

    def _get_contexts(self) -> None:
        pass

    def _get_units(self) -> None:
        pass

    def _get_nonnumeric(self) -> None:
        pass

    def _get_numeric(self) -> None:
        pass


class IXBRLParser(BaseParser):
    root_element: str = "html"

    def __init__(self, soup: BeautifulSoup, raise_on_error: bool = True) -> None:  # noqa: FBT001, FBT002
        self.soup = soup
        self.raise_on_error = raise_on_error
        self.errors: list = []
        self.contexts: dict[str, ixbrlContext] = {}
        self.schema: str | None = None
        self.namespaces: dict[str, str | list[str]] = {}
        self.nonnumeric: list[ixbrlNonNumeric] = []
        self.numeric: list[ixbrlNumeric] = []

    def _get_schema(self) -> None:
        self.schema = None
        schema_tag = self.soup.find(["link:schemaRef", "schemaRef", "link:schemaref", "schemaref"])
        if isinstance(schema_tag, Tag) and schema_tag.get("xlink:href"):
            schema = schema_tag["xlink:href"]
            if isinstance(schema, str):
                self.schema = schema.strip()

        self.namespaces = {}
        namespace_tag = self.soup.find(self.root_element)
        if isinstance(namespace_tag, Tag):
            for k in namespace_tag.attrs:
                if isinstance(k, str) and (k.startswith("xmlns") or ":" in k):
                    namespace_value = namespace_tag[k]
                    if isinstance(namespace_value, str):
                        self.namespaces[k] = namespace_value.split(" ")

    def _get_context_elements(
        self,
    ) -> Generator[Tag, None, None]:
        resources = self.soup.find(["ix:resources", "resources"])
        if isinstance(resources, Tag):
            for s in resources.find_all(["xbrli:context", "context"]):
                if isinstance(s, Tag):
                    yield s

    def _get_contexts(self) -> None:
        self.contexts = {}
        for s in self._get_context_elements():
            if not s.get("id"):
                continue
            s_id = s["id"]
            if not isinstance(s_id, str):
                continue  # pragma: no cover
            try:
                self.contexts[s_id] = ixbrlContext(
                    _id=s_id,
                    entity={
                        "scheme": self._get_tag_attribute(s, ["xbrli:identifier", "identifier"], "scheme"),
                        "identifier": self._get_tag_text(s, ["xbrli:identifier", "identifier"]),
                    },
                    segments=[
                        {"tag": x.name, "value": x.text.strip(), **x.attrs}
                        for x in self._get_tag_children(s, ["xbrli:segment", "segment"])
                    ],
                    instant=self._get_tag_text(s, ["xbrli:instant", "instant"]),
                    startdate=self._get_tag_text(s, ["xbrli:startDate", "startDate"]),
                    enddate=self._get_tag_text(s, ["xbrli:endDate", "endDate"]),
                )
            except Exception as e:
                self.errors.append(
                    ixbrlError(
                        error=e,
                        element=s,
                    )
                )
                if self.raise_on_error:
                    raise

    def _get_unit_elements(self) -> Generator[Tag, None, None]:
        resources = self.soup.find(["ix:resources", "resources"])
        if isinstance(resources, Tag):
            for s in resources.find_all(["xbrli:unit", "unit"]):
                if isinstance(s, Tag):
                    yield s

    def _get_units(self) -> None:
        self.units: dict[str, str | None] = {}
        for s in self._get_unit_elements():
            s_id = s.get("id")
            if isinstance(s_id, str):
                self.units[s_id] = self._get_tag_text(s, ["xbrli:measure", "measure"])

    def _get_tag_continuation(self, s: BeautifulSoup | Tag, start_str: str = "") -> str:
        if not isinstance(s, Tag):
            return start_str
        start_str += s.text
        if s.attrs.get("continuedAt"):
            continuation_tag = self.soup.find(id=s.attrs.get("continuedAt"))
            if isinstance(continuation_tag, Tag) and continuation_tag.name == "continuation":
                return self._get_tag_continuation(continuation_tag, start_str)
        return start_str

    def _get_nonnumeric(self) -> None:
        self.nonnumeric = []
        for s in self.soup.find_all({"nonNumeric"}):
            try:
                context = self.contexts.get(s["contextRef"], s["contextRef"])
                format_ = s.get("format")
                if not isinstance(format_, str):
                    format_ = None
                exclusion = s.find("exclude")
                if exclusion is not None:
                    exclusion.extract()

                text = s.text
                if s.attrs.get("continuedAt"):
                    text = self._get_tag_continuation(s)

                self.nonnumeric.append(
                    ixbrlNonNumeric(
                        context=context,
                        name=s["name"] if isinstance(s["name"], str) else "",
                        format_=format_,
                        value=text.strip().replace("\n", "") if isinstance(text, str) else "",
                        soup_tag=s,
                    )
                )
            except Exception as e:
                self.errors.append(
                    ixbrlError(
                        error=e,
                        element=s,
                    )
                )
                if self.raise_on_error:
                    raise

    def _get_numeric(self) -> None:
        self.numeric = []
        for s in self.soup.find_all({"nonFraction"}):
            try:
                self.numeric.append(
                    ixbrlNumeric(
                        text=s.text,
                        context=self.contexts.get(s["contextRef"], s["contextRef"]),
                        unit=self.units.get(s["unitRef"], s["unitRef"]),
                        soup_tag=s,
                        **s.attrs,
                    )
                )
            except Exception as e:
                self.errors.append(
                    ixbrlError(
                        error=e,
                        element=s,
                    )
                )
                if self.raise_on_error:
                    raise


class XBRLParser(IXBRLParser):
    root_element = "xbrl"

    def _get_context_elements(self) -> Generator[Tag, None, None]:
        for s in self.soup.find_all(["xbrli:context", "context"]):
            if isinstance(s, Tag):
                yield s

    def _get_unit_elements(self) -> Generator[Tag, None, None]:
        for s in self.soup.find_all(["xbrli:unit", "unit"]):
            if isinstance(s, Tag):
                yield s

    def _get_elements(self) -> Generator[Tag, None, None]:
        resource = self.soup.find(self.root_element)
        if isinstance(resource, Tag):
            for s in resource.find_all(True):
                if isinstance(s, Tag):
                    yield s

    def _get_numeric(self) -> None:
        self.numeric = []
        for s in self._get_elements():
            if not s.get("contextRef") or not s.get("unitRef"):
                continue
            context_ref = s["contextRef"]
            unit_ref = s["unitRef"]
            if not isinstance(context_ref, str) or not isinstance(unit_ref, str):
                continue  # pragma: no cover
            try:
                self.numeric.append(
                    ixbrlNumeric(
                        name=s.name,
                        text=s.text,
                        context=self.contexts.get(context_ref, context_ref),
                        unit=self.units.get(unit_ref, unit_ref),
                        soup_tag=s,
                        **s.attrs,
                    )
                )
            except Exception as e:
                self.errors.append(
                    {
                        "error": e,
                        "element": s,
                    }
                )
                if self.raise_on_error:
                    raise

    def _get_nonnumeric(self) -> None:
        self.nonnumeric = []
        for s in self._get_elements():
            try:
                if not s.get("contextRef") or s.get("unitRef"):
                    continue
                context_ref = s["contextRef"]
                if not isinstance(context_ref, str):
                    continue  # pragma: no cover
                context = self.contexts.get(context_ref, context_ref)
                format_ = s.get("format")
                if not isinstance(format_, str):
                    format_ = None

                text = s.text

                self.nonnumeric.append(
                    ixbrlNonNumeric(
                        context=context,
                        name=s.name if isinstance(s.name, str) else "",
                        format_=format_,
                        value=text.strip().replace("\n", "") if isinstance(text, str) else "",
                        soup_tag=s,
                    )
                )
            except Exception as e:
                self.errors.append(
                    ixbrlError(
                        error=e,
                        element=s,
                    )
                )
                if self.raise_on_error:
                    raise


class IXBRL:
    """
    Parse an iXBRL file.
    """

    def __init__(self, f: IO, raise_on_error: bool = True) -> None:  # noqa: FBT001, FBT002
        """Constructor for the IXBRL class.

        Parameters:
            f:  File-like object to parse.
            raise_on_error:  Whether to raise an exception on error
        """
        self.soup = BeautifulSoup(f.read(), "xml", multi_valued_attributes=None)
        self.raise_on_error = raise_on_error
        self._get_parser()
        self.parser._get_schema()
        self.parser._get_contexts()
        self.parser._get_units()
        self.parser._get_nonnumeric()
        self.parser._get_numeric()

    @classmethod
    def open(cls, filename: str | Path, raise_on_error: bool = True):  # noqa: FBT001, FBT002
        """Open an iXBRL file.

        Parameters:
            filename:  Path to file to parse.
            raise_on_error:  Whether to raise an exception on error
        """
        with open(filename, "rb") as a:
            return cls(a, raise_on_error=raise_on_error)

    def _get_parser(self) -> None:
        if self.soup.find("html"):
            self.filetype = FILETYPE_IXBRL
            parser = IXBRLParser
        elif self.soup.find("xbrl"):
            self.filetype = FILETYPE_XBRL
            parser = XBRLParser
        else:
            msg = "Filetype not recognised"
            raise IXBRLParseError(msg)
        self.parser: BaseParser = parser(self.soup, raise_on_error=self.raise_on_error)

    def __getattr__(self, name: str):
        return getattr(self.parser, name)

    def to_json(self) -> dict:
        """Return a JSON representation of the iXBRL file.

        Returns:
            A dictionary containing the following keys:

                - schema:  The schema used in the iXBRL file.
                - namespaces:  The namespaces used in the iXBRL file.
                - contexts:  The contexts used in the iXBRL file.
                - units:  The units used in the iXBRL file.
                - nonnumeric:  The non-numeric elements in the iXBRL file.
                - numeric:  The numeric elements in the iXBRL file.
                - errors:  The number of errors encountered when parsing the iXBRL file.
        """
        return {
            "schema": self.schema,
            "namespaces": self.namespaces,
            "contexts": {c: ct.to_json() for c, ct in self.contexts.items()},
            "units": self.units,
            "nonnumeric": [a.to_json() for a in self.nonnumeric],
            "numeric": [a.to_json() for a in self.numeric],
            "errors": len(self.errors),
        }

    def to_table(self, fields: str = "numeric") -> list[dict]:
        """Return a list of dictionaries representing the iXBRL file.

        This is suitable for passing to pandas.DataFrame.from_records().

        Parameters:
            fields:  Which fields to include in the output.  Can be "numeric", "nonnumeric" or "all".

        Returns:
            A list of dictionaries representing the iXBRL file.

        The fields included are:

        - schema (str)
        - name (str) -- the name of the element
        - value -- the value of the element. Can be number, str, None, or boolean
        - unit (str) -- the unit of the element if present
        - instant (date) -- the instant date of the element context if present
        - startdate (date) -- the start date of the element context if present
        - enddate (date) -- the end date of the element context if present
        - segment:N (str) -- the Nth segment of the element context if present (can be repeated)

        Examples:
            >>> import pandas as pd
            >>> i = IXBRL.open("tests/fixtures/ixbrl/uk-gaap/2009-12-31/Company-Accounts-Data.xml")
            >>> df = pd.DataFrame.from_records(i.to_table(fields="numeric"))
            >>> df.head()
        """
        if fields == "nonnumeric":
            values = self.nonnumeric
        elif fields == "numeric":
            values = self.numeric
        else:
            values = self.nonnumeric + self.numeric

        ret = []
        for v in values:
            if isinstance(v.context, ixbrlContext) and v.context.segments:
                segments = {
                    f"segment:{i}": "{} {} {}".format(s.get("tag", ""), s.get("dimension"), s.get("value")).strip()
                    for i, s in enumerate(v.context.segments)
                }
            else:
                segments = {"segment:0": ""}

            ret.append(
                {
                    "schema": " ".join(self.namespaces.get(f"xmlns:{v.schema}", [v.schema])),
                    "name": v.name,
                    "value": v.value,
                    "unit": v.unit if hasattr(v, "unit") else None,
                    "instant": str(v.context.instant)
                    if isinstance(v.context, ixbrlContext) and v.context.instant
                    else None,
                    "startdate": str(v.context.startdate)
                    if isinstance(v.context, ixbrlContext) and v.context.startdate
                    else None,
                    "enddate": str(v.context.enddate)
                    if isinstance(v.context, ixbrlContext) and v.context.enddate
                    else None,
                    **segments,
                }
            )
        return ret
