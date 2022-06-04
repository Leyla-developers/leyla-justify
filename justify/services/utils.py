import copy
import subprocess
from typing import Any, Union

from aeval import aeval
from textwrap3 import wrap
from .paginator import JustifyPaginatorInterface
import disnake
from disnake.ext import commands


class JustifyUtils:

    __version__ = 'justify-1.0'

    def  __init__(self) -> None:
        ...

    async def eval_code(self, ctx: commands.Context, code: str) -> Any:
        env = {
            'bot': ctx.bot, 
            'ctx': ctx, 
            'commands': commands,
            'disnake': disnake,
            '__import__': __import__,
            'sys': __import__('sys'),
            'os': __import__('os'),
            'aiohttp': __import__('aiohttp'),
            'requests': __import__('requests'),
            'datetime': __import__('datetime'),
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'subprocess': subprocess,
            'channel': ctx.channel,
            'random': __import__('random'),
            'asyncio': __import__('asyncio')
        }
        
        return await aeval(self.remove_token_references(code), env, {})


    def remove_token_references(self, text: str):
        return text.replace("bot.http.token", "'🤮'")
    

    async def _python_handler_result(self, ctx: commands.Context, result: str, prefix: str ='', suffix: str ='', length: int = 2000):
        paginator = None

        if isinstance(result, disnake.Message):
            return await ctx.reply(f'Message={result.jump_url}')

        if not isinstance(result, str):
            result = repr(result)

        if ctx.bot.http.token:
            result = result.replace(ctx.bot.http.token, '🤮')
        
        if len(result) >= 1994:
            paginator = JustifyPaginatorInterface(pages := [f"```{p}```" for p in wrap(result, length)])
            result = pages[0]

        await ctx.reply(f'{prefix}\n{result}{suffix}', view=paginator)


    async def shell_reader(self, ctx, commands: str) -> str:
        cmds = commands.split()
        byte_to_str = subprocess.check_output(cmds).decode('utf-8')
        result = '$ ' + "\n".join(cmds) + '\n\n' + byte_to_str

        return await self._python_handler_result(ctx, result, length=1900)


    async def alternative_context(
        self,
        ctx: commands.Context, 
        author: Union[disnake.User, disnake.Member] = None, 
        channel: disnake.TextChannel = None, 
        **kwargs
    ):
        message = copy.copy(ctx.message)
        message._update(kwargs)

        if author:
            message.author = author
        
        if channel:
            message.channel = channel

        return await ctx.bot.get_context(message, cls=type(ctx))
