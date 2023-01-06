from redis import asyncio as aioredis
import app.utils.Logger as Logger
from app.dependencies import load_config
from app.utils.RedisConnector import RedisConnector
from app.models.BallotModel import BallotModel

config: dict = load_config()

class Ballot:
    """Implements a ballot for ReVanced Polling API."""
    
    redis = RedisConnector.connect(config['ballots']['database'])
    
    BallotLogger = Logger.BallotLogger()
    
    async def store(self, discord_hashed_id: str, ballot: BallotModel) -> bool:
        """Store a ballot.
        
        Args:
            discord_hashed_id (str): Discord hashed ID of the voter
            ballot (dict): Ballot to store
        
        Returns:
            bool: True if the ballot was stored successfully, False otherwise
        """
        
        stored: bool = False
        
        try:
            await self.redis.json().set(
                name=discord_hashed_id,
                path=".",
                obj=ballot.dict(),
                nx=True
                )
            await self.BallotLogger.log("STORE_BALLOT", None, discord_hashed_id)
            stored = True
        except aioredis.RedisError as e:
            await self.BallotLogger.log("STORE_BALLOT", e)
            raise e
        
        return stored

    async def exists(self, discord_hashed_id: str):
        """Check if the ballot exists.
        
        Args:
            discord_hashed_id (str): Discord hashed ID of the voter
        
        Returns:
            bool: True if the ballot exists, False otherwise
        """
        
        exists: bool = False
        
        try:
            if await self.redis.exists(discord_hashed_id):
                exists = True
        except aioredis.RedisError as e:
            await self.BallotLogger.log("BALLOT_EXISTS", e)
            raise e
        
        return exists
