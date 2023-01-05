import os
import hmac
from fastapi_paseto_auth import AuthPASETO
from fastapi import APIRouter, Request, Response, Depends, status, HTTPException, Header
from app.dependencies import load_config
from app.controllers.Clients import Clients
from app.controllers.Ballot import Ballot
import app.models.ClientModels as ClientModels
import app.models.GeneralErrors as GeneralErrors
import app.models.ResponseModels as ResponseModels

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)
clients = Clients()
ballot = Ballot()
config: dict = load_config()

@router.post('/', response_model=ResponseModels.ClientAuthTokenResponse, status_code=status.HTTP_200_OK)
async def auth(request: Request, response: Response, client: ClientModels.ClientAuthModel, Authorize: AuthPASETO = Depends()) -> dict:
    """Authenticate a client and get an auth token.

    Returns:
        access_token: auth token
    """
    
    if(
        hmac.compare_digest(client.id, os.environ['CLIENT_ID']) and
        hmac.compare_digest(client.secret, os.environ['CLIENT_SECRET'])
        ):
        
        authenticated: bool = True
        
        if not authenticated:
            raise HTTPException(status_code=401, detail={
                "error": GeneralErrors.Unauthorized().error,
                "message": GeneralErrors.Unauthorized().message
                }
                                )
        else:
            if not ballot.exists(client.discord_id_hash):
                user_claims: dict[str, str] = {}
                user_claims['discord_id_hash'] = client.discord_id_hash
                access_token = Authorize.create_access_token(subject=client.id,
                                                            user_claims=user_claims,
                                                            fresh=True)
                return {"access_token": access_token}
            else:
                raise HTTPException(status_code=412, detail={
                    "error": GeneralErrors.PreconditionFailed().error,
                    "message": GeneralErrors.PreconditionFailed().message
                    }
                )
    else:
        raise HTTPException(status_code=401, detail={
            "error": GeneralErrors.Unauthorized().error,
            "message": GeneralErrors.Unauthorized().message
            }
                            )

@router.put("/exchange", response_model=ResponseModels.ClientAuthTokenResponse, status_code=status.HTTP_200_OK)
async def exchange_token(request: Request, response: Response, Authorize: AuthPASETO = Depends(), Authorization: str = Header(None)) -> dict:
    """Exchange a token for a new one.
    
    Returns:
        access_token: auth token
    
    """
    Authorize.paseto_required()

    user_claims: dict[str, str | bool] = {}
    user_claims['discord_id_hash'] = Authorize.get_user_claims()['discord_id_hash']
    user_claims['is_exchange_token'] = True
    access_token = Authorize.create_access_token(subject=Authorize.get_subject(),
                                                 user_claims=user_claims,
                                                 fresh=True)
    if not ballot.exists(Authorize.get_subject()):
        if await clients.ban_token(Authorize.get_jti()):
            return {"access_token": access_token}
        else: 
            raise HTTPException(status_code=500, detail={
                "error": GeneralErrors.InternalServerError().error,
                "message": GeneralErrors.InternalServerError().message
                }
                                )
    else:
        raise HTTPException(status_code=412, detail={
            "error": GeneralErrors.PreconditionFailed().error,
            "message": GeneralErrors.PreconditionFailed().message
            }
        )

@router.delete("/revoke", response_model=ResponseModels.RevokedTokenResponse, status_code=status.HTTP_200_OK)
async def revoke_token(request: Request, response: Response, Authorize: AuthPASETO = Depends(), Authorization: str = Header(None)) -> dict:
    """Revoke a token.
    
    Returns:
        revoked: bool
    
    """
    Authorize.paseto_required()

    if await clients.ban_token(Authorize.get_jti()):
        return {"revoked": True}
    else: 
        raise HTTPException(status_code=500, detail={
            "error": GeneralErrors.InternalServerError().error,
            "message": GeneralErrors.InternalServerError().message
            }
                            )

