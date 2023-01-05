from pydantic import BaseModel
from app.models.BallotFields import BallotFields

class BallotModel(BaseModel):
    """Implements the fields for the ballots.
    
    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    votes: list[BallotFields]
