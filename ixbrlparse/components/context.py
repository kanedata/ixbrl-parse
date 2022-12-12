import datetime
from copy import deepcopy
from typing import Any, Dict, List, Optional


class ixbrlContext:
    def __init__(
        self,
        _id: str,
        entity: Dict[str, Optional[str]],
        segments: Optional[List[Dict]],
        instant: Optional[str],
        startdate: Optional[str],
        enddate: Optional[str],
    ):
        self.id = _id
        self.entity = entity
        self.segments = segments
        self.instant: Optional[datetime.date] = (
            datetime.datetime.strptime(instant.strip(), "%Y-%m-%d").date()
            if instant
            else None
        )
        self.startdate: Optional[datetime.date] = (
            datetime.datetime.strptime(startdate.strip(), "%Y-%m-%d").date()
            if startdate
            else None
        )
        self.enddate: Optional[datetime.date] = (
            datetime.datetime.strptime(enddate.strip(), "%Y-%m-%d").date()
            if enddate
            else None
        )

    def __repr__(self) -> str:
        if self.startdate and self.enddate:
            datestr = "{} to {}".format(self.startdate, self.enddate)
        else:
            datestr = str(self.instant)

        segmentstr = " (with segments)" if self.segments else ""

        return "<IXBRLContext {} [{}]{}>".format(self.id, datestr, segmentstr)

    def to_json(self) -> Dict[str, List[Dict[str, Any]]]:
        values = deepcopy(self.__dict__)
        if values["segments"]:
            values["segments"] = [
                {
                    "tag": s.get("tag"),
                    "dimension": s.get("dimension"),
                    "value": s.get("value"),
                }
                for s in values["segments"]
            ]
        else:
            values["segments"] = {"tag": None, "dimension": None, "value": None}
        for i in ["startdate", "enddate", "instant"]:
            if isinstance(values[i], datetime.date):
                values[i] = str(values[i])
        return values
