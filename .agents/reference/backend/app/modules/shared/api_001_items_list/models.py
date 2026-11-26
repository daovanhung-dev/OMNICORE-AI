from pydantic import BaseModel
from app.core.responses import Envelope

class ListParams(BaseModel):
    page: int
    page_size: int

class Item(BaseModel):
    id: int
    name: str

class ItemPage(BaseModel):
    items: list[Item]
    total: int
    page: int
    page_size: int

ItemResponse = Envelope[ItemPage]
