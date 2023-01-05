from pydantic import BaseModel

class InternalServerError(BaseModel):
    """Implements the response fields for when an internal server error occurs.

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    error: str = "Internal Server Error"
    message: str = "An internal server error occurred. Please try again later."
    
class Conflict(BaseModel):
    """Implements the response fields for when a conflict occurs.

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    error: str = "Conflict"
    message: str = "User already voted on this ballot."
    
class PreconditionFailed(BaseModel):
    """Implements the response fields for when a precondition fails.

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    error: str = "Precondition Failed"
    message: str = "User is not eligible to vote on this ballot."
    
class Unauthorized(BaseModel):
    """Implements the response fields for when the client is unauthorized.

    Args:
        BaseModel (pydantic.BaseModel): BaseModel from pydantic
    """
    
    error: str = "Unauthorized"
    message: str = "The client is unauthorized to access this resource"

