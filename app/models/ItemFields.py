from pydantic import BaseModel

class LogoFields(BaseModel):
    """Implements the fields for the logos.
    
    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    id: str
    filename: str
    gdrive_direct_url: str

class ItemFields(BaseModel):
    """Implements the fields for the items.
    
    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    logos: list[LogoFields]
