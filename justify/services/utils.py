import sys
import os
import aiohttp
import requests
from typing import Any, Union
import datetime

from aeval import aeval
import nextcord
from nextcord.ext import commands


class JustifyUtils:

    __version__ = 'justify-1.1'

    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot

    async def eval_code(self, ctx: commands.Context, code: str) -> Any | None:
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'commands': commands,
            'nextcord': nextcord,
            '__import__': __import__,
            'sys': sys,
            'os': os,
            'aiohttp': aiohttp,
            'requests': requests,
            'datetime': datetime,
            'author': ctx.author,
            'guild': ctx.guild,
            'channel': ctx.message
        }
        
        return await aeval(code, env, {})

    async def python_handler_result(self, ctx: commands.Context, result: str):
        if isinstance(result, nextcord.Message):
            return await ctx.reply(f'Сообщение({result.jump_url})')
        
        if self.bot.http.token:
            result = result.replace(self.bot.http.token, 'э, токен получай на https://discord.com/developers/applications')
        
        await ctx.reply(result)
