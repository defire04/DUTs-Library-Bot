from telegram_bot.actions.action_creator import ButtonAction
from types import FunctionType


def create_filter_query_by_action(action_id: int, filtering_callback: FunctionType | None = None):
    def filter_query_by_action(callback):
        action = ButtonAction.from_json(callback.data)
        check_result = callback.data and action.id == action_id
        if not filtering_callback or not check_result:
            return check_result
        return filtering_callback(action)

    return filter_query_by_action