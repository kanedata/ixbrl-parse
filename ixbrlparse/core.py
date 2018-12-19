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
        for s in resources.find_all({'xbrli:context'}):
            self.contexts[s['id']] = ixbrlContext(**{
                "_id": s['id'],
                "entity": s.find('xbrli:identifier').text if s.find('xbrli:identifier') else None,
                "segment": s.find('xbrli:segment').text.strip() if s.find('xbrli:segment') else None,
                "dimension": s.find({'xbrldi:explicitmember'}).get('dimension') if s.find({'xbrldi:explicitmember'}) else None,
                "instant": s.find('xbrli:instant').text if s.find('xbrli:instant') else None,
                "startdate": s.find('xbrli:startdate').text if s.find('xbrli:startdate') else None,
                "enddate": s.find('xbrli:enddate').text if s.find('xbrli:enddate') else None,
            })
        for s in resources.find_all({'context'}):
            self.contexts[s['id']] = ixbrlContext(**{
                "_id": s['id'],
                "entity": s.find('identifier').text if s.find('identifier') else None,
                "segment": s.find('segment').text.strip() if s.find('segment') else None,
                "dimension": s.find({'explicitmember'}).get('dimension') if s.find({'explicitmember'}) else None,
                "instant": s.find('instant').text if s.find('instant') else None,
                "startdate": s.find('startdate').text if s.find('startdate') else None,
                "enddate": s.find('enddate').text if s.find('enddate') else None,
            })

    def _get_units(self):
        self.units = {}
        resources = self.soup.find('ix:resources')
        for s in resources.find_all({'xbrli:unit'}):
            self.units[s['id']] = s.find('xbrli:measure').text if s.find('xbrli:measure') else None
        for s in resources.find_all({'unit'}):
            self.units[s['id']] = s.find('measure').text if s.find('measure') else None

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


class ixbrlContext:

    def __init__(self, _id, entity, segment, dimension, instant, startdate, enddate):
        self._id = _id
        self.entity = entity
        self.segment = segment
        self.dimension = dimension
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
        return "<IXBRLContext {} [{}]>".format(self._id, datestr)

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
        name = attrs.get('name').split(":", maxsplit=1)
        if len(name) == 2:
            self.schema = name[0]
            self.name = name[1]
        else:
            self.schema = 'unknown'
            self.name = name[0]

        self.text = attrs.get('text')
        self.value = attrs.get('value')
        self.context = attrs.get('context')
        self.unit = attrs.get('unit')
        self.format = {
            "format": attrs.get('format'),
            "decimals": int(attrs.get('decimals')),
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
            self.value = self.value * (10 ^ self.format['scale'])
