import datetime
from copy import deepcopy
from typing import Any, Dict, List, Optional


class ixbrlContext:  # noqa: N801
    """Class to represent an ixbrl context.

    The context should either have an instant date or a start and end date.

    Attributes:
        id: The id of the context.
        entity: A dictionary of the entity information.
        segments: A list of dictionaries of the segment information.
        instant: The instant date of the context.
        startdate: The start date of the context.
        enddate: The end date of the context."""

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
        self.instant: Optional[datetime.date] = None
        self.startdate: Optional[datetime.date] = None
        self.enddate: Optional[datetime.date] = None

        date_fields = {
            "instant": instant,
            "startdate": startdate,
            "enddate": enddate,
        }
        for field, value in date_fields.items():
            if value:
                datevalue = datetime.datetime.strptime(value.strip(), "%Y-%m-%d").astimezone().date()
                setattr(self, field, datevalue)

    def __repr__(self) -> str:
        if self.startdate and self.enddate:
            datestr = f"{self.startdate} to {self.enddate}"
        else:
            datestr = str(self.instant)

        segmentstr = " (with segments)" if self.segments else ""

        return f"<IXBRLContext {self.id} [{datestr}]{segmentstr}>"

    def to_json(self) -> Dict[str, List[Dict[str, Any]]]:
        """Convert the object to a JSON serialisable dictionary."""
        values = deepcopy(self.__dict__)
        for i in ["startdate", "enddate", "instant"]:
            if isinstance(values[i], datetime.date):
                values[i] = str(values[i])
        return values
