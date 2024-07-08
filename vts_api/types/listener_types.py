from pydantic import BaseModel, SkipValidation


class Handler(BaseModel):
    skippable: bool
    function: SkipValidation
