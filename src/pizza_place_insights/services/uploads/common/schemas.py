from pydantic import BaseModel


class DefaultResponse(BaseModel):
    loaded_rows_count: int
