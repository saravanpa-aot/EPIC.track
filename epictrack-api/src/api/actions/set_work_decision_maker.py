"""Disable work start date action handler"""

from api.actions.base import ActionFactory
from api.models.event import Event


class SetWorkDecisionMaker(ActionFactory):  # pylint: disable=too-few-public-methods
    """Sets the work decision maker"""

    def run(self, source_event: Event, params: dict) -> None:
        """Performs the required operations"""
        return

    def get_additional_params(self, params):
        """Returns additional parameter"""
        return params