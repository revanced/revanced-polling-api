from collections import deque
from pydantic import BaseModel

class BallotFields(BaseModel):
    """Implements the fields for the ballots.
    
    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    cid: str
    weight: int
