from fastapi_paseto_auth import AuthPASETO
from fastapi import APIRouter, Request, Response, Depends, status, HTTPException
from app.dependencies import load_config
from app.models.BallotModel import BallotModel
import app.models.GeneralErrors as GeneralErrors
import app.models.ResponseModels as ResponseModels
import app.controllers.Ballot as Ballot
import app.controllers.Clients as Clients

router = APIRouter()

ballot_controller = Ballot.Ballot()

client = Clients.Clients()

config: dict = load_config()

@router.post('/ballot', response_model=ResponseModels.BallotCastedResponse,
             tags=['Ballot'], status_code=status.HTTP_201_CREATED)
async def cast_ballot(request: Request, response: Response,
                              ballot: BallotModel,
                              Authorize: AuthPASETO = Depends()) -> dict:
    """Casts a ballot.

    Returns:
        json: ballot casted
    """
    Authorize.paseto_required()
    
    
    if (Authorize.get_token_payload()['is_exchange_token'] and
        not await ballot_controller.exists(
            Authorize.get_token_payload()['discord_id_hash']
            )):
        
        stored: bool = await ballot_controller.store(
            Authorize.get_token_payload()['discord_id_hash'],
            ballot)
            
        if stored:
            await client.ban_token(Authorize.get_jti())
            return {"cast": stored}
        else:
            raise HTTPException(status_code=500, detail={
                "error": GeneralErrors.InternalServerError().error,
                "message": GeneralErrors.InternalServerError().message
                }
                                )
    else:
        raise HTTPException(status_code=401, detail={
            "error": GeneralErrors.Unauthorized().error,
            "message": GeneralErrors.Unauthorized().message
        }
                            )
