"""Disable work start date action handler"""

from api.actions.base import ActionFactory
from api.models.work import Work


class LockWorkStartDate(ActionFactory):  # pylint: disable=too-few-public-methods
    """Disable work start date action"""

    def run(self, source_event, params) -> None:
        """Set the work start date and mark start date as locked for changes"""
        work = Work.find_by_id(source_event.work_id)
        work.start_date_locked = params.get("start_date_locked")
        work.start_date = source_event.actual_date
        work.update(work.as_dict(recursive=False), commit=False)
