from typing import Any, Union
from datetime import datetime

from aeval import aeval
import disnake
from disnake.ext import commands


class Justify:

    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot
        
        
    async def eval_code(self, ctx: commands.Context, code: str) -> Any | None:
        
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'commands': commands,
            'disnake': disnake,
            '__import__': __import__
        }
        
        return await aeval(code, env, {})
