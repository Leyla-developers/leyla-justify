import disnake
from disnake.ext import commands
from disnake.ui import *

    
class JustifyPaginatorInterface(disnake.ui.View):    

    def __init__(self, pages: list[disnake.Embed]):
        self.pages = pages
        self.current_index = 0
        
        super().__init__(timeout=None)


    async def set_backward_buttons_state(self, state: bool) -> None:
        self.go_to_start.disabled = state
        self.previous_page.disabled = state


    async def set_forward_buttons_state(self, state: bool) -> None:
        self.go_to_end.disabled = state
        self.next_page.disabled = state


    @button(emoji="⏪", disabled=True)
    async def go_to_start(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        await self.set_backward_buttons_state(True)
        await self.set_forward_buttons_state(False)
        embed = self.pages[0]
        await inter.response.edit_message(embed=embed, view=self)

    
    @button(emoji="◀️")
    async def previous_page(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        self.current_index -= 1
        embed = self.pages[self.current_index]
        self.next_page.disabled = False
        self.previous_page.disabled = False

        if self.current_index == 0:
            self.previous_page.disabled = True
            self.next_page.disabled = False
        
        await inter.response.edit_message(view=self, embed=embed)

    @button(emoji="❌")
    async def stop_paginator(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.edit_message(view=None)

        
    @button(emoji="")
    async def next_page(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        self.current_index -= 1
        embed = self.pages[self.current_index]
        self.next_page.disabled = False
        self.previous_page.disabled = False

        if self.current_index == len(self.pages)-1:
            self.next_page.disable = True
            self.go_to_end.disabled = True
        
        await inter.response.edit_message(view=self, embed=embed)
    
        
    @button(emoji="⏩", disabled=True)
    async def go_to_end(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        await self.set_backward_buttons_state(False)
        await self.set_forward_buttons_state(True)

        embed = self.pages[-1]
        await inter.response.edit_message(embed=embed, view=self)
    
