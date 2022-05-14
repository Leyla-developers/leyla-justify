from .main.__main__ import Justify


class JustifyCog(Justify):
 
    """loads justify cog."""

def setup(bot):
    bot.add_cog(JustifyCog(bot))
