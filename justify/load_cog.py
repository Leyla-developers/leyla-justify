from disnake.ext import commands
from .main import __main__

UTILS = [__main__]

__all__ = ['Justify', '__main__', 'setup']

class Justify(commands.Cog, *UTILS):

    def __init__(self, bot) -> None:
        """This file loads justify cog"""
        self.bot = bot

def setup(bot):
    bot.add_cog(Justify(bot))
