from pydantic import BaseModel
from app.models.BallotFields import BallotFields

class BallotModel(BaseModel):
    """Implements the fields for the ballots.
    
    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    discord_id_hash: str
    ballot: list[BallotFields]
