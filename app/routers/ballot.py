from fastapi_paseto_auth import AuthPASETO
from fastapi import APIRouter, Request, Response, Depends, status, HTTPException
from app.dependencies import load_config
from app.models.BallotModel import BallotModel
import app.models.GeneralErrors as GeneralErrors
import app.models.ResponseModels as ResponseModels
import app.controllers.Ballot as Ballot

router = APIRouter()

ballot_controller = Ballot.Ballot()

config: dict = load_config()

@router.post('/ballot', response_model=ResponseModels.BallotCastedResponse,
             tags=['Ballot'], status_code=status.HTTP_201_CREATED)
async def create_announcement(request: Request, response: Response,
                              ballot: BallotModel,
                              Authorize: AuthPASETO = Depends()) -> dict:
    """Casts a ballot.

    Returns:
        json: announcement information
    """
    Authorize.paseto_required()
    
    discord_hashed_id: str = Authorize.get_paseto_claims()['discord_hashed_id']
    
    stored: bool = await ballot_controller.store(discord_hashed_id, ballot.vote)
        
    if stored:
        return {"created": stored}
    else:
        raise HTTPException(status_code=500, detail={
            "error": GeneralErrors.InternalServerError().error,
            "message": GeneralErrors.InternalServerError().message
            }
                            )
