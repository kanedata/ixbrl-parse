import datetime


class ixbrlContext:
    def __init__(self, _id, entity, segments, instant, startdate, enddate):
        self.id = _id
        self.entity = entity
        self.segments = segments
        # @TODO: parse dates here
        self.instant = (
            datetime.datetime.strptime(instant.strip(), "%Y-%m-%d").date()
            if instant
            else None
        )
        self.startdate = (
            datetime.datetime.strptime(startdate.strip(), "%Y-%m-%d").date()
            if startdate
            else None
        )
        self.enddate = (
            datetime.datetime.strptime(enddate.strip(), "%Y-%m-%d").date()
            if enddate
            else None
        )

    def __repr__(self):
        if self.startdate and self.enddate:
            datestr = "{} to {}".format(self.startdate, self.enddate)
        else:
            datestr = str(self.instant)

        segmentstr = " (with segments)" if self.segments else ""

        return "<IXBRLContext {} [{}]{}>".format(self.id, datestr, segmentstr)

    def to_json(self):
        values = self.__dict__
        for i in ["startdate", "enddate", "instant"]:
            if isinstance(values[i], datetime.date):
                values[i] = str(values[i])
        return values
