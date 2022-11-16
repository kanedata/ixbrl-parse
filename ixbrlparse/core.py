from pathlib import Path
from typing import IO, Dict, Generator, Iterable, List, Optional, Union

from bs4 import BeautifulSoup, Tag

from ixbrlparse.components import ixbrlContext, ixbrlNonNumeric, ixbrlNumeric

FILETYPE_IXBRL = "ixbrl"
FILETYPE_XBRL = "xbrl"


class IXBRLParseError(Exception):
    pass


class BaseParser:
    def _get_tag_attribute(
        self, s: Union[BeautifulSoup, Tag], tag: Union[str, List[str]], attribute: str
    ) -> Optional[str]:
        tag_contents = s.find(tag)
        if isinstance(tag_contents, Tag):
            attribute_value = tag_contents.get(attribute)
            if isinstance(attribute_value, str):
                return attribute_value.strip()
        return None

    def _get_tag_text(
        self, s: Union[BeautifulSoup, Tag], tag: Union[str, List[str]]
    ) -> Optional[str]:
        tag_contents = s.find(tag)
        if isinstance(tag_contents, Tag):
            text_value = tag_contents.text
            if isinstance(text_value, str):
                return text_value.strip()
        return None

    def _get_tag_children(
        self, s: Union[BeautifulSoup, Tag], tag: Union[str, List[str]]
    ) -> Iterable[Tag]:
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

    def __init__(self, soup: BeautifulSoup, raise_on_error: bool = True) -> None:
        self.soup = soup
        self.raise_on_error = raise_on_error
        self.errors: List = []
        self.contexts: Dict[str, ixbrlContext] = {}
        self.schema: Optional[str] = None
        self.namespaces: Dict[str, Union[str, List[str]]] = {}
        self.nonnumeric: List[ixbrlNonNumeric] = []
        self.numeric: List[ixbrlNumeric] = []

    def _get_schema(self) -> None:
        self.schema = None
        schema_tag = self.soup.find(["link:schemaRef", "schemaRef"])
        if isinstance(schema_tag, Tag) and schema_tag.get("xlink:href"):
            if isinstance(schema_tag["xlink:href"], str):
                self.schema = schema_tag["xlink:href"].strip()

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
            if not isinstance(s["id"], str):
                continue  # pragma: no cover
            self.contexts[s["id"]] = ixbrlContext(
                _id=s["id"],
                entity={
                    "scheme": self._get_tag_attribute(
                        s, ["xbrli:identifier", "identifier"], "scheme"
                    ),
                    "identifier": self._get_tag_text(
                        s, ["xbrli:identifier", "identifier"]
                    ),
                },
                segments=[
                    {"tag": x.name, "value": x.text.strip(), **x.attrs}
                    for x in self._get_tag_children(s, ["xbrli:segment", "segment"])
                ],
                instant=self._get_tag_text(s, ["xbrli:instant", "instant"]),
                startdate=self._get_tag_text(s, ["xbrli:startDate", "startDate"]),
                enddate=self._get_tag_text(s, ["xbrli:endDate", "endDate"]),
            )

    def _get_unit_elements(self) -> Generator[Tag, None, None]:
        resources = self.soup.find(["ix:resources", "resources"])
        if isinstance(resources, Tag):
            for s in resources.find_all(["xbrli:unit", "unit"]):
                if isinstance(s, Tag):
                    yield s

    def _get_units(self) -> None:
        self.units: Dict[str, Optional[str]] = {}
        for s in self._get_unit_elements():
            if isinstance(s["id"], str):
                self.units[s["id"]] = self._get_tag_text(
                    s, ["xbrli:measure", "measure"]
                )

    def _get_nonnumeric(self) -> None:
        self.nonnumeric = []
        for s in self.soup.find_all({"nonNumeric"}):
            try:
                context = self.contexts.get(s["contextRef"], s["contextRef"])
                format_ = s.get("format")
                if not isinstance(format_, str):
                    format_ = None
                self.nonnumeric.append(
                    ixbrlNonNumeric(
                        context=context,
                        name=s["name"] if isinstance(s["name"], str) else "",
                        format_=format_,
                        value=s.text.strip().replace("\n", "")
                        if isinstance(s.text, str)
                        else "",
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

    def _get_numeric(self) -> None:
        self.numeric = []
        for s in self.soup.find_all({"nonFraction"}):
            try:
                self.numeric.append(
                    ixbrlNumeric(
                        text=s.text,
                        context=self.contexts.get(s["contextRef"], s["contextRef"]),
                        unit=self.units.get(s["unitRef"], s["unitRef"]),
                        **s.attrs
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
            if not isinstance(s["contextRef"], str) or not isinstance(
                s["unitRef"], str
            ):
                continue  # pragma: no cover
            try:
                self.numeric.append(
                    ixbrlNumeric(
                        name=s.name,
                        text=s.text,
                        context=self.contexts.get(s["contextRef"], s["contextRef"]),
                        unit=self.units.get(s["unitRef"], s["unitRef"]),
                        **s.attrs
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
            if not s.get("contextRef") or s.get("unitRef"):
                continue
            if not isinstance(s["contextRef"], str):
                continue  # pragma: no cover
            context = self.contexts.get(s["contextRef"], s["contextRef"])
            format_ = s.get("format")
            if not isinstance(format_, str):
                format_ = None
            self.nonnumeric.append(
                ixbrlNonNumeric(
                    context=context,
                    name=s.name if isinstance(s.name, str) else "",
                    format_=format_,
                    value=s.text.strip().replace("\n", "")
                    if isinstance(s.text, str)
                    else "",
                )
            )


class IXBRL:
    def __init__(self, f: IO, raise_on_error: bool = True) -> None:
        self.soup = BeautifulSoup(f.read(), "xml", multi_valued_attributes=None)
        self.raise_on_error = raise_on_error
        self._get_parser()
        self.parser._get_schema()
        self.parser._get_contexts()
        self.parser._get_units()
        self.parser._get_nonnumeric()
        self.parser._get_numeric()

    @classmethod
    def open(cls, filename: Union[str, Path], raise_on_error: bool = True):
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
            raise IXBRLParseError("Filetype not recognised")
        self.parser: BaseParser = parser(self.soup, raise_on_error=self.raise_on_error)

    def __getattr__(self, name: str):
        return getattr(self.parser, name)

    def to_json(self) -> Dict:
        return {
            "schema": self.schema,
            "namespaces": self.namespaces,
            "contexts": {c: ct.to_json() for c, ct in self.contexts.items()},
            "units": self.units,
            "nonnumeric": [a.to_json() for a in self.nonnumeric],
            "numeric": [a.to_json() for a in self.numeric],
            "errors": len(self.errors),
        }

    def to_table(self, fields: str = "numeric") -> List[Dict]:
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
                    "segment:{}".format(i): "{} {} {}".format(
                        s.get("tag", ""), s.get("dimension"), s.get("value")
                    ).strip()
                    for i, s in enumerate(v.context.segments)
                }
            else:
                segments = {"segment:0": ""}

            ret.append(
                {
                    "schema": " ".join(
                        self.namespaces.get("xmlns:{}".format(v.schema), [v.schema])
                    ),
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
