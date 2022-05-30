from typing import List

import disnake
from disnake.ui import *


class JustifyPaginatorInterface(disnake.ui.View):    

    def __init__(self, pages: List[str]) -> None:
        self.pages = pages
        self.current_index = 0
        super().__init__(timeout=None)


    @button(emoji="⏪") # type: ignore
    async def go_to_start(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        data = self.pages[0]
        await inter.response.edit_message(content=data, view=self)

    
    @button(emoji="◀️") # type: ignore
    async def previous_page(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        self.current_index -= 1
        data = self.pages[self.current_index]        
        await inter.response.edit_message(content=data, view=self)


    @button(label='❌', style=disnake.ButtonStyle.red) # type: ignore
    async def stop_paginator(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await inter.delete_original_message()


    @button(emoji="▶️") # type: ignore
    async def next_page(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        self.current_index += 1
        data = self.pages[self.current_index]
        
        await inter.response.edit_message(content=data, view=self)

        
    @button(emoji="⏩") # type: ignore
    async def go_to_end(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        data = self.pages[-1]
        await inter.response.edit_message(content=data, view=self)
