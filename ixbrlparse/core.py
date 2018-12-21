import datetime
from bs4 import BeautifulSoup

class IXBRL():

    def __init__(self, f):
        self.soup = BeautifulSoup(f.read(), "html.parser")
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
        self.schema = self.soup.find('link:schemaref').get('xlink:href')
        self.namespaces = {}
        for k in self.soup.find('html').attrs:
            if k.startswith("xmlns") or ":" in k:
                self.namespaces[k] = self.soup.find('html')[k].split(" ")

    def _get_contexts(self):
        self.contexts = {}
        resources = self.soup.find('ix:resources')
        for s in resources.find_all(['xbrli:context', 'context']):
            self.contexts[s['id']] = ixbrlContext(**{
                "_id": s['id'],
                "entity": {
                    "scheme": s.find(['xbrli:identifier', 'identifier'])['scheme'] if s.find(['xbrli:identifier', 'identifier']) else None,
                    "identifier": s.find(['xbrli:identifier', 'identifier']).text if s.find(['xbrli:identifier', 'identifier']) else None,
                },
                "segments": [{
                    "tag": x.name,
                    "value": x.text.strip(),
                    **x.attrs
                } for x in s.find(['xbrli:segment', 'segment']).findChildren()] if s.find(['xbrli:segment', 'segment']) else None,
                "instant": s.find(['xbrli:instant', 'instant']).text if s.find(['xbrli:instant', 'instant']) else None,
                "startdate": s.find(['xbrli:startdate', 'startdate']).text if s.find(['xbrli:startdate', 'startdate']) else None,
                "enddate": s.find(['xbrli:enddate', 'enddate']).text if s.find(['xbrli:enddate', 'enddate']) else None,
            })

    def _get_units(self):
        self.units = {}
        resources = self.soup.find('ix:resources')
        for s in resources.find_all(['xbrli:unit', 'unit']):
            self.units[s['id']] = s.find(['xbrli:measure', 'measure']).text if s.find([
                'xbrli:measure', 'measure']) else None

    def _get_nonnumeric(self):
        self.nonnumeric = [ixbrlNonNumeric(**{
            "context": self.contexts.get(s['contextref'], s['contextref']),
            "name": s['name'],
            "format_": s.get('format'),
            "value": s.text.strip().replace("\n", "")
        }) for s in self.soup.find_all({'ix:nonnumeric'})]

    def _get_numeric(self):
        self.numeric = [ixbrlNumeric({
            "text": s.text,
            "context": self.contexts.get(s['contextref'], s['contextref']),
            "unit": self.units.get(s['unitref'], s['unitref']),
            **s.attrs
        }) for s in self.soup.find_all({'ix:nonfraction'})]

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
                "schema": " ".join(self.namespaces.get("xmlns:{}".format(v.schema), [v.schema])),
                "name": v.name,
                "value": v.value,
                "unit": v.unit if hasattr(v, 'unit') else None,
                "instant": str(v.context.instant) if v.context.instant else None,
                "startdate": str(v.context.startdate) if v.context.startdate else None,
                "enddate": str(v.context.enddate) if v.context.enddate else None,
                **segments
            })
        return ret



class ixbrlContext:

    def __init__(self, _id, entity, segments, instant, startdate, enddate):
        self.id = _id
        self.entity = entity
        self.segments = segments
        # @TODO: parse dates here
        self.instant = datetime.datetime.strptime(
            instant, "%Y-%m-%d").date() if instant else None
        self.startdate = datetime.datetime.strptime(
            startdate, "%Y-%m-%d").date() if startdate else None
        self.enddate = datetime.datetime.strptime(
            enddate, "%Y-%m-%d").date() if enddate else None

    def __repr__(self):
        if self.startdate and self.enddate:
            datestr = "{} to {}".format(self.startdate, self.enddate)
        else:
            datestr = str(self.instant)

        segmentstr = " (with segments)" if self.segments else ""

        return "<IXBRLContext {} [{}]{}>".format(self.id, datestr, segmentstr)

    def to_json(self):
        values = self.__dict__
        for i in ['startdate', 'enddate', 'instant']:
            if isinstance(values[i], datetime.date):
                values[i] = str(values[i])
        return values

class ixbrlNonNumeric:

    def __init__(self, context, name, format_, value):

        name = name.split(":", maxsplit=1)
        if len(name) == 2:
            self.schema = name[0]
            self.name = name[1]
        else:
            self.schema = 'unknown'
            self.name = name[0]

        self.context = context
        self.format = format_
        self.value = value

    def to_json(self):
        values = self.__dict__
        values['context'] = self.context.to_json()
        return values

class ixbrlNumeric:

    # contextref
    # decimals
    # format
    # name
    # scale
    # sign
    # text
    # unitref
    # xmlns:ix
    def __init__(self, attrs):
        name = attrs.get('name', "").split(":", maxsplit=1)
        if len(name) == 2:
            self.schema = name[0]
            self.name = name[1]
        else:
            self.schema = 'unknown'
            self.name = name[0]

        decimals = attrs.get('decimals', "0")
        if decimals.lower() == "inf":
            decimals = None
        else:
            decimals = int(decimals)

        self.text = attrs.get('text')
        self.value = attrs.get('value')
        self.context = attrs.get('context')
        self.unit = attrs.get('unit')
        self.format = {
            "format": attrs.get('format'),
            "decimals": decimals,
            "scale": int(attrs.get('scale', 0)),
            "sign": attrs.get('sign', ""),
        }
        self._parse_value()

    def _parse_value(self):
        if not self.value:
            # @TODO: Maybe do more comprehensive regex replace here
            self.value = self.text.replace(',', '')

        if self.value == '-':
            self.value = 0

        if isinstance(self.value, str):
            self.value = self.value.replace(',', '')
            self.value = float(self.value)

        if self.format['sign'] == "-":
            self.value = self.value * -1

        if self.format['scale'] != 0:
            self.value = self.value * (10 ** self.format['scale'])

    def to_json(self):
        values = self.__dict__
        values['context'] = self.context.to_json()
        return values
