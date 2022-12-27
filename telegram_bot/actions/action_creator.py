from abc import abstractmethod, ABC
from typing import Generic, TypeVar
import json

from util.multimethod import MultipleMeta
from models.actions import Actions


class Payload(ABC):
    @abstractmethod
    def to_shorthand_payload(self) -> dict:
        pass


class ButtonPageActionPayload(metaclass=MultipleMeta):

    def __init__(self, page_index: int, prepared_collection_id: int, sort_direction: int):
        super().__init__()
        self.page_index = page_index
        self.prepared_collection_id = prepared_collection_id
        self.sort_direction = sort_direction
        pass

    def __init__(self, rawPayload: dict) -> None:
        super().__init__()
        self.__init__(rawPayload["pg"], rawPayload["d"], rawPayload["sd"])
        pass

    def to_shorthand_payload(self):
        return {
            "pg": self.page_index,
            "d": self.prepared_collection_id,
            "sd": self.sort_direction
        }


class ButtonMenuActionPayload:

    def __init__(self) -> None:
        pass

    def to_shorthand_payload(self):
        return {}


class ButtonCategoryActionPayload(metaclass=MultipleMeta):

    def __init__(self, categry_id: int, category_type: int):
        super().__init__()
        self.categry_id = categry_id
        self.category_type = category_type
        pass

    def __init__(self, rawPayload: dict) -> None:
        super().__init__()
        self.__init__(rawPayload["id"], rawPayload["ty"])
        pass

    def to_shorthand_payload(self):
        return {
            "id": self.categry_id,
            "ty": self.category_type
        }


PAYLOADS = {
    Actions.SWITCH_PAGE: ButtonPageActionPayload,
    Actions.TO_CATEGORY_MENU: ButtonCategoryActionPayload,
    Actions.CHANGE_SORT_DIRECTION: ButtonPageActionPayload
}

P = TypeVar('P')


class ButtonAction(Generic[P]):
    def __init__(self, action_id: int, payload: P):
        self.id = action_id
        self.payload = payload

    @classmethod
    def from_json(cls, json_action: str):
        try:
            parsed_action = json.loads(json_action)
        except:
            return cls(-1, None)
        if (parsed_action.__class__ is not dict):
            return cls(-1, None)
        action = parsed_action["a"]
        payload = parsed_action["pl"]
        PayloadClass = PAYLOADS.get(action)
        if not PayloadClass:
            return cls(action, None)
        return cls(action, PayloadClass(payload))

    def stringify(self):
        return json.dumps({
            "a": self.id,
            "pl": self.payload.to_shorthand_payload() if self.payload else self.payload
        }).replace(' ', '')


class ButtonPageAction(ButtonAction[ButtonPageActionPayload]):
    def __init__(self, action_id: int, page_index: int, prepared_collection_id: int, sort_direction: int = 0):
        payload = ButtonPageActionPayload(
            page_index, prepared_collection_id, sort_direction)
        super().__init__(action_id, payload)


class ButtonPageChangeAction(ButtonPageAction):
    def __init__(self, page_index: int, prepared_collection_id: int, sort_direction: int = 0):
        super().__init__(Actions.SWITCH_PAGE, page_index, prepared_collection_id, sort_direction)


class ButtonPageSortDirectionAction(ButtonPageAction):
    def __init__(self, page_index: int, prepared_collection_id: int, sort_direction: int = 0):
        super().__init__(Actions.CHANGE_SORT_DIRECTION, page_index, prepared_collection_id, sort_direction)


class ButtonMenuAction(ButtonAction[None]):
    def __init__(self, action: int):
        payload = None
        super().__init__(action, payload)


class ButtonCategoryAction(ButtonAction[ButtonCategoryActionPayload]):
    def __init__(self, category_id: int, category_type: str):
        payload = ButtonCategoryActionPayload(
            category_id, category_type)
        super().__init__(Actions.TO_CATEGORY_MENU, payload)
