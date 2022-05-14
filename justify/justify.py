import time
from typing import Union
from .main.__main__ import Justify
from disnake.ext import commands


class JustifyCog(commands.Cog):
    
    """Loads justify cog."""

    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot
        self.justify = Justify(bot)


    @commands.group( name='justify', aliases=['jst'], invoke_without_command=True)
    async def jst(self, ctx: commands.Context):
        text = \
            f"**Enabled intents:** {', '.join([i[0] for i in self.bot.intents if i[-1]])}\n" \
            f'**Guilds:** {len(self.bot.guilds)}\n' \
            f'**Users:** {len(self.bot.users)}\n' \
            f'**Cached messages:** {len(self.bot.cached_messages)}\n' + \
            (f'**Bot shards:** {", ".join(list(self.bot.shards))}' if isinstance(self.bot, commands.AutoShardedBot) else "")
            
        await ctx.reply(content=text)
    
    
    @jst.command(name='eval', aliases=['py'])
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, text: str):
        code = text.strip("\n").strip("```").lstrip("\n").lstrip("py") if text.startswith("```py") else text
        start = time.time()
        
        try:
            result = str(await self.justify.eval_code(ctx, code))
            
        except Exception as exception:
            result = f"# Произошла ошибка при выполнении кода: \n{exception.__class__}: {exception}"
        
        finally:
            execution_time = round(time.time() - start, 2)
            await ctx.send(f"Выполнено за **{execution_time} сек.**\n```py\n{result}\n```")
        

def setup(bot):
    bot.add_cog(JustifyCog(bot))
