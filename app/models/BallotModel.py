from pydantic import BaseModel

class BallotModel(BaseModel):
    """Implements the fields for the ballots.
    
    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    vote: str
