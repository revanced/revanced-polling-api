from redis import asyncio as aioredis
import app.utils.Logger as Logger
from app.dependencies import load_config
from app.utils.RedisConnector import RedisConnector
import app.controllers.Ballot as Ballot

config: dict = load_config()

class Clients:
    
    """Implements a client for ReVanced Polling API."""
    
    redis = RedisConnector.connect(config['tokens']['database'])
    ballot = Ballot.Ballot()
    
    UserLogger = Logger.UserLogger()
    
    async def ban_token(self, token: str) -> bool:
        """Ban a token

        Args:
            token (str): Token to ban

        Returns:
            bool: True if the token was banned successfully, False otherwise
        """
        
        banned: bool = False
        
        try:
            if type(config['auth']['access_token_expires']) is bool:
                await self.redis.set(name=token, value="", nx=True)
            else:
                await self.redis.set(name=token,
                                        value="",
                                        nx=True,
                                        ex=config['auth']['access_token_expires'])
            await self.UserLogger.log("BAN_TOKEN", None, token)
            banned = True
        except aioredis.RedisError as e:
            await self.UserLogger.log("BAN_TOKEN", e)
            raise e
        
        return banned

    async def is_token_banned(self, token: str) -> bool:
        """Check if the token is banned

        Args:
            token (str): Token to check

        Returns:
            bool: True if the token is banned, False otherwise
        """
        
        banned: bool = False
        
        try:
            if await self.redis.exists(token):
                banned = True
        except aioredis.RedisError as e:
            await self.UserLogger.log("IS_TOKEN_BANNED", e)
            raise e
        
        return banned

    async def voted(self, token: str, discord_id: str) -> bool:
        """Check if the user already voted

        Args:
            token (str): Token to check

        Returns:
            bool: True if the user voted, False otherwise
        """
        
        voted: bool = False
        
        try:
            if (await self.is_token_banned(token) or
                await self.ballot.exists(discord_id)):
                
                voted = True
        except aioredis.RedisError as e:
            await self.UserLogger.log("AUTH_CHECKS", e)
            raise e
        
        return voted
