import time
from typing import Union
import sys

import disnake
from .services.utils import JustifyUtils
from disnake.ext import commands


class JustifyCog(commands.Cog):
    """Loads justify cog."""
    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot
        self.justify = JustifyUtils(bot)
    
    @commands.is_owner()
    @commands.group(name='justify', aliases=['jst'], invoke_without_command=True)
    async def justify_main_command(self, ctx: commands.Context):
        text = [
            f'`{self.justify.__version__}, disnake-{disnake.__version__}, {sys.version}.`\n',
            f'Guilds: **{len(self.bot.guilds)}**, users: **{len(self.bot.users)}**',
            f'Cached messages: **{len(self.bot.cached_messages)}**',
            f'```py\nEnabled intents: {", ".join([i[0] for i in self.bot.intents if i[-1]])}```'
        ]

        if isinstance(self.bot, commands.AutoShardedBot):
            text.append(f'Shards:\n' + '```py\n' + '\n'.join(list(f"{i[0]} - {i[-1]}" for i in self.bot.latencies)) + '```')

        await ctx.reply('\n'.join(text))

    @justify_main_command.command(name='eval', aliases=['py'])
    async def justify_eval(self, ctx: commands.Context, *, text: str):
        code = text.strip("\n").strip("```").lstrip("\n").lstrip("py") if text.startswith("```py") else text # Колбаска ^-^
        start = time.time()
        safety_code = code.replace(self.bot.http.token, 'token deleted.')

        try:
            result = str(await self.justify.eval_code(ctx, safety_code))
            
        except Exception as exception:
            result = f"# An error occurred while executing the code :: \n{exception.__class__}: {exception}"
        
        finally:
            execution_time = round((time.time() - start)*1000, 2)
            await ctx.send(f"Completed for **{execution_time} seconds.**\n{result}\n")


def setup(bot):
    bot.add_cog(JustifyCog(bot))
