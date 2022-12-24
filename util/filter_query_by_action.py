from actions.action_creator import ButtonAction
from models.actions import Actions
from types import FunctionType


def create_filter_query_by_action(action_id: int, filtering_callback: FunctionType | None = None):
    def filter_query_by_action(callback):
        action = ButtonAction.from_json(callback.data)
        check_result = callback.data and action.id == action_id
        if check_result and not filtering_callback:
            return check_result
        
        return filtering_callback(action)

    return filter_query_by_action