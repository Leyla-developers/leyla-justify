from disnake.ext import commands


class Justify:

    def  __init__(self, bot) -> None:
        self.bot = bot

    @commands.group(name='justify', alises=['jst'], invoke_without_command=True)
    async def main_justify(self, ctx):
        await ctx.reply('Test successfully ended.')
