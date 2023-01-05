from pydantic import BaseModel
import app.models.ResponseFields as ResponseFields

"""Implements pydantic models and model generator for the API's responses."""

class PingResponseModel(BaseModel):
    """Implements the JSON response model for the /heartbeat endpoint.

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    status: int
    detail: str

class ClientAuthTokenResponse(BaseModel):
    """Implements the response fields for client auth tokens.

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    access_token: str
    
class RevokedTokenResponse(BaseModel):
    """Implements the response fields for token invalidation.

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    revoked: bool

class BallotCastedResponse(BaseModel):
    """Implements the response fields for ballot casted.

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    cast: bool
