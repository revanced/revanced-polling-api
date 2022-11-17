import json
import aiofiles
from fastapi import APIRouter, Request, Response
from fastapi_cache.decorator import cache
from app.dependencies import load_config
from app.models.ItemModels import ItemModel

router = APIRouter()

config: dict = load_config()

@router.get('/logos', response_model=ItemModel, tags=['Logos'])
@cache(config['cache']['expire'])
async def logos(request: Request, response: Response) -> dict:
    """Get logos.

    Returns:
        json: list of logos
    """
    
    async with aiofiles.open('app/data/processed.json', 'r') as json_file:
        data: dict = {}
        data = json.loads(await json_file.read())

    return data
