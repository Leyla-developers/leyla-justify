from typing import Union
from datetime import datetime

from aeval import aeval
import disnake
from disnake.ext import commands


class Justify:

    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot

    @commands.group(
        name='justify', 
        aliases=['jst'], 
        invoke_without_command=True, 
    )
    async def justify_main_command(self, ctx):
        main_info = (
            f'Enabled intents: {list(i[0] for i in self.bot.intents if i[-1])}',
            f'Guilds: {self.bot.guilds} | Members: {len(self.bot.users)}',
            f'Cached messages: {len(self.bot.cached_messages)}',
        )
        
        if isinstance(self.bot, commands.AutoShardedBot):
            main_info.append(f'Bot shards: {", ".join(list(self.bot.shards))}')

        await ctx.reply(main_info)

    @commands.command(name='eval', aliases=['py'])
    async def justify_eval(self, ctx, *, code):
        if ctx.author.id not in self.bot.owner_ids:
            raise commands.NotOwner('You must be a bot owner for use justify.')
        else:
            start = datetime.now()
            replaced_code = "\n".join(code.split("\n")[1:])[:-3] if code.startswith("```") and code.endswith("```") else code
            env = {
                'bot': self.bot,
                'ctx': ctx,
                'commands': commands,
                'disnake': disnake,
                '__import__': __import__
            }

            try:
                result = await aeval(replaced_code, env, {})
                end = (datetime.now() - start).seconds

                await ctx.reply(result)
                await ctx.send(f'Completed for `{end}` seconds')
            except Exception as e:
                end = (datetime.now() - start).seconds
                raise e
