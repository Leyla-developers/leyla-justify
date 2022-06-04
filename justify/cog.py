import time
from typing import Union
import sys
from pathlib import Path

import disnake
from .services.utils import JustifyUtils
from disnake.ext import commands


class JustifyCog(commands.Cog):
    """Loads justify cog."""
    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot
        self.justify = JustifyUtils()


    async def cog_check(self, ctx: commands.Context) -> bool:
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner('You must be a bot owner to use justify')

        return True


    @commands.group(name='justify', aliases=['jst'], invoke_without_command=True)
    async def justify_main_command(self, ctx: commands.Context):
        text = [
            f'`{self.justify.__version__}, disnake-{disnake.__version__}, {sys.version}.`\n',
            f'Guilds: **{len(self.bot.guilds)}**, users: **{len(self.bot.users)}**',
            f'Cached messages: **{len(self.bot.cached_messages)}**',
            f'```py\nEnabled intents: {", ".join([i[0] for i in self.bot.intents if i[-1]])}```'
        ]

        if isinstance(self.bot, commands.AutoShardedBot):
            text.append(f'Shards:\n' + '```py\n' + '\n'.join(list(f"{i[0]} - {i[-1]*1000}" for i in self.bot.latencies)) + '```')

        await ctx.reply('\n'.join(text))

    @justify_main_command.command(name='eval', aliases=['py'])
    async def justify_eval(self, ctx: commands.Context, *, text: str):
        code = text.strip("\n").strip("```").lstrip("\n").lstrip("py") if text.startswith("```py") else text # Колбаска ^-^

        try:
            result = str(await self.justify.eval_code(ctx, code))

        except Exception as exception:
            result = f"```py\n# An error occurred while executing the code :: \n{exception.__class__}: {exception}```" 
        
        finally:
            await self.justify._python_handler_result(ctx, result, length=1980)

    @justify_main_command.command(name='debug', aliases=['dbg'])
    async def justify_debug(self, ctx: commands.Context, *, cmd: str):
        command = self.bot.get_command(cmd)

        if not command:
            return await ctx.reply('Command not found.')
        
        start = time.perf_counter()

        await ctx.invoke(command)

        end = time.perf_counter()
        await ctx.reply(f"Command `{command}` completed in `{end - start:.3f}` seconds")

    @justify_main_command.command(name="load", aliases=['ld'])
    async def justify_load(self, ctx: commands.Context, *, paths):
        list_of_paths = paths.split(paths)
        for i in list_of_paths:
            try:
                await self.bot.load_extension(i)
            except:
                await self.bot.unload_extension(i)
                await self.bot.load_extension(i)
        
        await ctx.reply(' '.join(list_of_paths) + f'cog{"" if len(paths) == 0 else "s"} was loaded ✅')

    @justify_main_command.command(name="unload", aliases=['uld'])
    async def justify_unload(self, ctx: commands.Context, *, paths):
        list_of_paths = paths.split(paths)
        for i in list_of_paths:
            try:
                await self.bot.unload_extension(i)
            except:
                await self.bot.load_extension(i)
                await self.bot.unload_extension(i)
        
        await ctx.reply(' '.join(list_of_paths) + f'cog{"" if len(paths) == 0 else "s"} was unloaded ✅')

    @justify_main_command.command(name="reload", aliases=['rld'])
    async def justify_reload(self, ctx: commands.Context, *, paths):
        list_of_paths = paths.split(paths)
        for i in list_of_paths:
            await self.bot.reload_extension(i)
        
        await ctx.reply(' '.join(list_of_paths) + f'cog{"" if len(paths) == 0 else "s"} was reloaded ✅')

    @justify_main_command.command(name='cat')
    async def justify_cat(self, ctx, path):
        source = list(Path().glob(pattern=path))
        if '.env' in path:
            return await ctx.reply(f'File `{path}` not found.')
        elif len(source):
            await self.justify._python_handler_result(ctx, open(path).read(), prefix='```py', suffix='```', length=1980)
        else:
            await ctx.reply(f'File `{path}` not found.')

    # @justify_main_command.command(name='src')
    # async def justify_command_source(self, ctx):


    @justify_main_command.command(name='shell', aliases=['sh', 'bash'])
    async def justify_shell(self, ctx, *, commands: str):
        await self.justify._python_handler_result(ctx, 
            result=await self.justify.shell_reader(
                ctx=ctx, commands=commands
            ), prefix='```bash', suffix='```'
        )


def setup(bot):
    bot.add_cog(JustifyCog(bot=bot))
