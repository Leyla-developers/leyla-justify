from disnake.ext import commands
from .main.__main__ import Justify

__all__ = ('Justify', 'setup')

class JustifyCog:

    """This file loads justify cog"""

def setup(bot):
    bot.add_cog(JustifyCog(bot))
