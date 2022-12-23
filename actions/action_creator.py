from abc import abstractmethod, ABC
from typing import Generic, TypeVar
import json

from util.multimethod import MultipleMeta




class Actions:
    SWITCH_PAGE = 0


class Payload(ABC):
    @abstractmethod
    def to_shorthand_payload(self) -> dict:
        pass


class ButtonPageActionPayload(metaclass=MultipleMeta):

    def __init__(self, page_index: int, prepared_collection_id: int):
        super().__init__()
        self.page_index = page_index
        self.prepared_collection_id = prepared_collection_id
        pass

    def __init__(self, rawPayload: dict) -> None:
        super().__init__()
        self.__init__(rawPayload["pg"], rawPayload["d"])
        pass

    def to_shorthand_payload(self):
        return {
            "pg": self.page_index,
            "d": self.prepared_collection_id
        }


PAYLOADS = {
    Actions.SWITCH_PAGE: ButtonPageActionPayload
}

P = TypeVar('P')


class ButtonAction(Generic[P]):
    def __init__(self, action_id: int, payload: P):
        self.id = action_id
        self.payload = payload

    @classmethod
    def from_json(cls, json_action: str):
        parsed_action = json.loads(json_action)
        action = parsed_action["a"]
        payload = parsed_action["pl"]
        PayloadClass = PAYLOADS.get(action)
        return cls(action, PayloadClass(payload))

    def stringify(self):
        return json.dumps({
            "a": self.id,
            "pl": self.payload.to_shorthand_payload()
        }).replace(' ', '')


class ButtonPageAction(ButtonAction[ButtonPageActionPayload]):
    def __init__(self, page_index: int, prepared_collection_id: int):
        payload = ButtonPageActionPayload(
            page_index, prepared_collection_id)
        super().__init__(Actions.SWITCH_PAGE, payload)



