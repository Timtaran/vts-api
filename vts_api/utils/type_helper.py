from pydantic import BaseModel

from vts_api.types import class_by_event_name_list


def class_by_event_name(event_name: str) -> BaseModel:
    return class_by_event_name_list[event_name]
