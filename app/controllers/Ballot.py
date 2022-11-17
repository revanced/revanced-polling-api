from redis import asyncio as aioredis
import app.utils.Logger as Logger
from app.dependencies import load_config
from app.utils.RedisConnector import RedisConnector

config: dict = load_config()

class Ballot:
    """Implements a ballot for ReVanced Polling API."""
    
    redis = RedisConnector.connect(config['tokens']['database'])
    
    BallotLogger = Logger.BallotLogger()
    
    async def store(self, discord_hashed_id: str, ballot: str) -> bool:
        """Store a ballot.
        
        Args:
            discord_hashed_id (str): Discord hashed ID of the voter
            ballot (dict): Ballot to store
        
        Returns:
            bool: True if the ballot was stored successfully, False otherwise
        """
        
        stored: bool = False
        
        try:
            await self.redis.set(name=discord_hashed_id, value=ballot, nx=True)
            await self.BallotLogger.log("STORE_BALLOT", None, discord_hashed_id)
            stored = True
        except aioredis.RedisError as e:
            await self.BallotLogger.log("STORE_BALLOT", e)
            raise e
        
        return stored
