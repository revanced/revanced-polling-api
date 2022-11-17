from pydantic import BaseModel
from app.models.ItemFields import ItemFields

class ItemModel(BaseModel):
    """Implements the model for the items.
    
    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    __root__: dict[str, ItemFields]

