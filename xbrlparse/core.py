from bs4 import BeautifulSoup

class XBRL():

    def __init__(self, f):
        self.soup = BeautifulSoup(f.read(), "html.parser")
        self._get_contexts()
        self._get_units()
        self._get_nonnumeric()
        self._get_numeric()

    def _get_contexts(self):
        self.contexts = {s['id']: xbrlContext(**{
            "_id": s['id'],
            "entity": s.find('xbrli:identifier').text if s.find('xbrli:identifier') else None,
            "segment": s.find('xbrli:segment').text.strip() if s.find('xbrli:segment') else None,
            "dimension": s.find({'xbrldi:explicitmember'}).get('dimension') if s.find({'xbrldi:explicitmember'}) else None,
            "instant": s.find('xbrli:instant').text if s.find('xbrli:instant') else None,
            "startdate": s.find('xbrli:startdate').text if s.find('xbrli:startdate') else None,
            "enddate": s.find('xbrli:enddate').text if s.find('xbrli:enddate') else None,
        }) for s in self.soup.find_all({'xbrli:context'})}

    def _get_units(self):
        self.units = {
            s['id']: s.find('xbrli:measure').text if s.find('xbrli:measure') else None
            for s in self.soup.find_all({'xbrli:unit'})
        }

    def _get_nonnumeric(self):
        self.nonnumeric = [xbrlNonNumeric(**{
            "context": self.contexts.get(s['contextref'], s['contextref']),
            "name": s['name'],
            "format_": s.get('format'),
            "value": s.text.strip().replace("\n", "")
        }) for s in self.soup.find_all({'ix:nonnumeric'})]

    def _get_numeric(self):
        self.numeric = [xbrlNumeric({
            "text": s.text,
            "context": self.contexts.get(s['contextref'], s['contextref']),
            "unit": self.units.get(s['unitref'], s['unitref']),
            **s.attrs
        }) for s in self.soup.find_all({'ix:nonfraction'})]


class xbrlContext:

    def __init__(self, _id, entity, segment, dimension, instant, startdate, enddate):
        self._id = _id
        self.entity = entity
        self.segment = segment
        self.dimension = dimension
        # @TODO: parse dates here
        self.instant = instant
        self.startdate = startdate
        self.enddate = enddate

    def __repr__(self):
        if self.startdate and self.enddate:
            datestr = "{} to {}".format(self.startdate, self.enddate)
        else:
            datestr = str(self.instant)
        return "<XBRLContext {} [{}]>".format(self._id, datestr)

class xbrlNonNumeric:

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

class xbrlNumeric:

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
            "decimals": attrs.get('decimals'),
            "scale": attrs.get('scale', 0),
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
