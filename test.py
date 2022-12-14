from abc import abstractmethod, ABC
import time
from typing import Generic, List, Type, TypeVar, _SpecialGenericAlias
import json

from multimethod import MultipleMeta

# class SearchResult:
#     def __init__(self, books: List[Book], search_query: str):
#         self.data = books
#         self.search_query = search_query
#         self.data_length = len(books)


# class PagesResult:
#     def __init__(self, result: SearchResult, results_per_page: int = 4):
#         self.result = result
#         self.results_per_page = results_per_page

#     def get_page(self, index: int):
#         page = self.result.data[index *
#                                 self.results_per_page: (index + 1) * self.results_per_page]
#         return page


class Actions:
    SWITCH_PAGE = 0


class Payload(ABC):
    @abstractmethod
    def to_shorthand_payload() -> dict:
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
    def __init__(self, action: int, payload: P):
        self.action = action
        self.payload = payload

    @classmethod
    def from_json(cls, jsonAction: str):
        parsed_action = json.loads(jsonAction)
        action = parsed_action["a"]
        payload = parsed_action["pl"]
        PayloadClass = PAYLOADS.get(action)
        return cls(action, PayloadClass(payload))

    def stringify(self):
        return json.dumps({
            "a": self.action,
            "pl": self.payload.to_shorthand_payload()
        }).replace(' ', '')


class ButtonPageAction(ButtonAction[ButtonPageActionPayload]):
    def __init__(self, page_index: int, prepared_collection_id: int):
        payload = ButtonPageActionPayload(
            page_index, prepared_collection_id)
        super().__init__(Actions.SWITCH_PAGE, payload)


action = ButtonAction.from_json(
    '{"a": 0, "pl": {"pg": 1, "d": 12}}')
print(len(action.stringify()))
