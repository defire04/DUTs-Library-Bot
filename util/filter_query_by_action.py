from actions.action_creator import ButtonAction
from models.actions import Actions


def create_filter_query_by_action(action_id: int):
    def filter_query_by_action(callback):
        return callback.data and ButtonAction.from_json(callback.data).id == action_id
    return filter_query_by_action