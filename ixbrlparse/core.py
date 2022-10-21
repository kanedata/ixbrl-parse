from bs4 import BeautifulSoup

from ixbrlparse.components import ixbrlContext, ixbrlNonNumeric, ixbrlNumeric

FILETYPE_IXBRL = "ixbrl"
FILETYPE_XBRL = "xbrl"


class IXBRLParser:
    """Core class for parsing XBRL and iXBRL files

    Takes a BeautifulSoup object created from an XBRL or iXBRL file

    Keyword Arguments:
        soup {BeautifulSoup} -- BeautifulSoup object created from an XBRL or iXBRL file
        raise_on_error {bool} -- Raise an error if an error is encountered (default: {True})

    Public attributes:
        soup {BeautifulSoup} -- BeautifulSoup object created from an XBRL or iXBRL file
        raise_on_error {bool} -- Raise an error if an error is encountered
        errors {list} -- List of errors encountered
        schema {str} -- XBRL schema
        namespaces {dict} -- Namespaces used in the file
        contexts {dict} -- Contexts used in the file (uses the ixbrlContext class)
        units {dict} -- Units used in the file (as a dictionary of strings)
        nonnumeric {list} -- Non-numeric elements (uses the ixbrlNonNumeric class)
        numerics {list} -- Numeric elements (uses the ixbrlNumeric class)

    Methods:
        parse -- Parse the file
    """

    root_element = "html"

    def __init__(self, soup, raise_on_error=True):
        self.soup = soup
        self.raise_on_error = raise_on_error
        self.errors = []

    def parse(self):
        """Run all the parsing methods in the correct order"""
        self._get_schema()
        self._get_contexts()
        self._get_units()
        self._get_nonnumeric()
        self._get_numeric()

    def _get_schema(self):
        """Get the XBRL schema from the file

        Also collects other namespaces used in the file"""
        self.schema = self.soup.find(["link:schemaRef", "schemaRef"]).get("xlink:href")
        self.namespaces = {}
        for k in self.soup.find(self.root_element).attrs:
            if k.startswith("xmlns") or ":" in k:
                self.namespaces[k] = self.soup.find(self.root_element)[k].split(" ")

    def _get_context_elements(self):
        """Generator to get all the context elements in the file"""
        resources = self.soup.find(["ix:resources", "resources"])
        for s in resources.find_all(["xbrli:context", "context"]):
            yield s

    def _get_contexts(self):
        """Get all the contexts in the file

        This should be run before _get_nonnumeric and _get_numeric"""
        self.contexts = {}
        for s in self._get_context_elements():
            self.contexts[s["id"]] = ixbrlContext(
                **{
                    "_id": s["id"],
                    "entity": {
                        "scheme": s.find(["xbrli:identifier", "identifier"])[
                            "scheme"
                        ].strip()
                        if s.find(["xbrli:identifier", "identifier"])
                        else None,
                        "identifier": s.find(
                            ["xbrli:identifier", "identifier"]
                        ).text.strip()
                        if s.find(["xbrli:identifier", "identifier"])
                        else None,
                    },
                    "segments": [
                        {"tag": x.name, "value": x.text.strip(), **x.attrs}
                        for x in s.find(["xbrli:segment", "segment"]).findChildren()
                    ]
                    if s.find(["xbrli:segment", "segment"])
                    else None,
                    "instant": s.find(["xbrli:instant", "instant"]).text.strip()
                    if s.find(["xbrli:instant", "instant"])
                    else None,
                    "startdate": s.find(["xbrli:startDate", "startDate"]).text.strip()
                    if s.find(["xbrli:startDate", "startDate"])
                    else None,
                    "enddate": s.find(["xbrli:endDate", "endDate"]).text.strip()
                    if s.find(["xbrli:endDate", "endDate"])
                    else None,
                }
            )

    def _get_unit_elements(self):
        """Generator to fetch all the unit elements in the file"""
        resources = self.soup.find(["ix:resources", "resources"])
        for s in resources.find_all(["xbrli:unit", "unit"]):
            yield s

    def _get_units(self):
        """Extract the units used in the file"""
        self.units = {}
        for s in self._get_unit_elements():
            self.units[s["id"]] = (
                s.find(["xbrli:measure", "measure"]).text.strip()
                if s.find(["xbrli:measure", "measure"])
                else None
            )

    def _get_nonnumeric(self):
        """Extract all the non-numeric elements in the file

        Raises an error if the element can't be parsed and self.raise_on_error is True"""
        self.nonnumeric = []
        for s in self.soup.find_all({"nonNumeric"}):
            element = {
                "context": self.contexts.get(s["contextRef"], s["contextRef"]),
                "name": s["name"],
                "format_": s.get("format"),
                "value": s.text.strip().replace("\n", ""),
            }
            try:
                self.nonnumeric.append(ixbrlNonNumeric(**element))
            except Exception as e:
                self.errors.append(
                    {
                        "error": e,
                        "element": s,
                    }
                )
                if self.raise_on_error:
                    raise

    def _get_numeric(self):
        """Extract all the numeric elements in the file

        Raises an error if the element can't be parsed and self.raise_on_error is True"""
        self.numeric = []
        for s in self.soup.find_all({"nonFraction"}):
            element = {
                "text": s.text,
                "context": self.contexts.get(s["contextRef"], s["contextRef"]),
                "unit": self.units.get(s["unitRef"], s["unitRef"]),
                **s.attrs,
            }
            try:
                self.numeric.append(ixbrlNumeric(element))
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
    """Class to parse XBRL files

    Extends the IXBRLParser class to use different methods for parsing XBRL files"""

    root_element = "xbrl"

    def _get_context_elements(self):
        """Generator to get all the context elements in the file"""
        for s in self.soup.find_all(["xbrli:context", "context"]):
            yield s

    def _get_unit_elements(self):
        """Generator to fetch all the unit elements in the file"""
        for s in self.soup.find_all(["xbrli:unit", "unit"]):
            yield s

    def _get_elements(self):
        """Generator to fetch all the elements in the file"""
        for s in self.soup.find(self.root_element).find_all():
            yield s

    def _get_numeric(self):
        """Extract all the numeric elements in the file

        In an XBRL file, this is all the elements that have context or unit attributes

        Raises an error if the element can't be parsed and self.raise_on_error is True"""
        self.numeric = []
        for s in self._get_elements():
            if not s.get("contextRef") or not s.get("unitRef"):
                continue
            element = {
                "name": s.name,
                "text": s.text,
                "context": self.contexts.get(s["contextRef"], s["contextRef"]),
                "unit": self.units.get(s["unitRef"], s["unitRef"]),
                **s.attrs,
            }
            try:
                self.numeric.append(ixbrlNumeric(element))
            except Exception as e:
                self.errors.append(
                    {
                        "error": e,
                        "element": s,
                    }
                )
                if self.raise_on_error:
                    raise

    def _get_nonnumeric(self):
        """Extract all the non-numeric elements in the file

        In an XBRL file, this is all the elements that do not have context or unit attributes

        Raises an error if the element can't be parsed and self.raise_on_error is True"""
        self.nonnumeric = []
        for s in self._get_elements():
            if not s.get("contextRef") or s.get("unitRef"):
                continue
            element = {
                "context": self.contexts.get(s["contextRef"], s["contextRef"]),
                "name": s.name,
                "format_": s.get("format"),
                "value": s.text.strip().replace("\n", ""),
            }
            try:
                self.nonnumeric.append(ixbrlNonNumeric(**element))
            except Exception as e:
                self.errors.append(
                    {
                        "error": e,
                        "element": s,
                    }
                )
                if self.raise_on_error:
                    raise


class IXBRL:
    """Class to parse and store the results of an IXBRL file

    This class wraps around the IXBRLParser or XBRLParser classes to parse the file and store the results"""

    def __init__(self, f, raise_on_error=True):
        self.soup = BeautifulSoup(f.read(), "xml")
        self.raise_on_error = raise_on_error
        self._get_parser()
        self.parser.parse()

    @classmethod
    def open(cls, filename, raise_on_error=True):
        """Open an IXBRL file from a filename and return an IXBRL object"""
        with open(filename, "rb") as a:
            return cls(a, raise_on_error=raise_on_error)

    def _get_parser(self):
        """Choose the correct parser for the file

        - IXBRL files have an "html" element
        - XBRL files have an "xbrl" element"""
        if self.soup.find("html"):
            self.filetype = FILETYPE_IXBRL
            parser = IXBRLParser
        elif self.soup.find("xbrl"):
            self.filetype = FILETYPE_XBRL
            parser = XBRLParser
        else:
            raise Exception("Filetype not recognised")
        self.parser = parser(self.soup, raise_on_error=self.raise_on_error)

    def __getattr__(self, name):
        return getattr(self.parser, name)

    def to_json(self):
        """Return the results as a JSON string"""
        return {
            "schema": self.schema,
            "namespaces": self.namespaces,
            "contexts": {c: ct.to_json() for c, ct in self.contexts.items()},
            "units": self.units,
            "nonnumeric": [a.to_json() for a in self.nonnumeric],
            "numeric": [a.to_json() for a in self.numeric],
            "errors": len(self.errors),
        }

    def to_table(self, fields="numeric"):
        """Return the results as a list of dicts

        The fields argument can be "numeric", "nonnumeric" or "all" to return the numeric, non-numeric or all elements

        The fields included are:

        - schema (str)
        - name (str) -- the name of the element
        - value -- the value of the element. Can be number, str, None, or boolean
        - unit (str) -- the unit of the element if present
        - instant (date) -- the instant date of the element context if present
        - startdate (date) -- the start date of the element context if present
        - enddate (date) -- the end date of the element context if present
        - segment:N (str) -- the Nth segment of the element context if present (can be repeated)"""
        if fields == "nonnumeric":
            values = self.nonnumeric
        elif fields == "numeric":
            values = self.numeric
        else:
            values = self.nonnumeric + self.numeric

        ret = []
        for v in values:
            if v.context.segments:
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
                    "instant": str(v.context.instant) if v.context.instant else None,
                    "startdate": str(v.context.startdate)
                    if v.context.startdate
                    else None,
                    "enddate": str(v.context.enddate) if v.context.enddate else None,
                    **segments,
                }
            )
        return ret
