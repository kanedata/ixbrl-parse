import datetime
from bs4 import BeautifulSoup

from ixbrlparse.components import ixbrlContext, ixbrlNonNumeric, ixbrlNumeric


class IXBRL():

    def __init__(self, f):
        self.soup = BeautifulSoup(f.read(), "xml")
        self._get_schema()
        self._get_contexts()
        self._get_units()
        self._get_nonnumeric()
        self._get_numeric()

    @classmethod
    def open(cls, filename):
        with open(filename) as a:
            return cls(a)

    def _get_schema(self):
        self.schema = self.soup.find(
            ['link:schemaRef', 'schemaRef']).get('xlink:href')
        self.namespaces = {}
        for k in self.soup.find('html').attrs:
            if k.startswith("xmlns") or ":" in k:
                self.namespaces[k] = self.soup.find('html')[k].split(" ")

    def _get_contexts(self):
        self.contexts = {}
        resources = self.soup.find(['ix:resources', 'resources'])
        for s in resources.find_all(['xbrli:context', 'context']):
            self.contexts[s['id']] = ixbrlContext(**{
                "_id": s['id'],
                "entity": {
                    "scheme": s.find(
                        ['xbrli:identifier', 'identifier']
                    )['scheme'] if s.find(
                        ['xbrli:identifier', 'identifier']
                    ) else None,
                    "identifier": s.find(
                        ['xbrli:identifier', 'identifier']
                    ).text if s.find(
                        ['xbrli:identifier', 'identifier']
                    ) else None,
                },
                "segments": [{
                    "tag": x.name,
                    "value": x.text.strip(),
                    **x.attrs
                } for x in s.find(
                    ['xbrli:segment', 'segment']
                ).findChildren()] if s.find(
                    ['xbrli:segment', 'segment']
                ) else None,
                "instant": s.find(
                    ['xbrli:instant', 'instant']
                ).text if s.find(
                    ['xbrli:instant', 'instant']
                ) else None,
                "startdate": s.find(
                    ['xbrli:startDate', 'startDate']
                ).text if s.find(
                    ['xbrli:startDate', 'startDate']
                ) else None,
                "enddate": s.find(
                    ['xbrli:endDate', 'endDate']
                ).text if s.find(
                    ['xbrli:endDate', 'endDate']
                ) else None,
            })

    def _get_units(self):
        self.units = {}
        resources = self.soup.find(['ix:resources', 'resources'])
        for s in resources.find_all(['xbrli:unit', 'unit']):
            self.units[s['id']] = s.find(
                ['xbrli:measure', 'measure']
            ).text if s.find(
                ['xbrli:measure', 'measure']
            ) else None

    def _get_nonnumeric(self):
        self.nonnumeric = [ixbrlNonNumeric(**{
            "context": self.contexts.get(s['contextRef'], s['contextRef']),
            "name": s['name'],
            "format_": s.get('format'),
            "value": s.text.strip().replace("\n", "")
        }) for s in self.soup.find_all({'nonNumeric'})]

    def _get_numeric(self):
        self.numeric = [ixbrlNumeric({
            "text": s.text,
            "context": self.contexts.get(s['contextRef'], s['contextRef']),
            "unit": self.units.get(s['unitRef'], s['unitRef']),
            **s.attrs
        }) for s in self.soup.find_all({'nonFraction'})]

    def to_json(self):
        return {
            "schema": self.schema,
            "namespaces": self.namespaces,
            "contexts": {c: ct.to_json() for c, ct in self.contexts.items()},
            "units": self.units,
            "nonnumeric": [a.to_json() for a in self.nonnumeric],
            "numeric": [a.to_json() for a in self.numeric],
        }

    def to_table(self, fields="numeric"):
        if fields == 'nonnumeric':
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
                    ).strip() for i, s in enumerate(v.context.segments)
                }
            else:
                segments = {"segment:0": ""}

            ret.append({
                "schema": " ".join(
                    self.namespaces.get(
                        "xmlns:{}".format(v.schema),
                        [v.schema]
                    )
                ),
                "name": v.name,
                "value": v.value,
                "unit": v.unit if hasattr(v, 'unit') else None,
                "instant": str(v.context.instant)
                if v.context.instant else None,
                "startdate": str(v.context.startdate)
                if v.context.startdate else None,
                "enddate": str(v.context.enddate)
                if v.context.enddate else None,
                **segments
            })
        return ret
