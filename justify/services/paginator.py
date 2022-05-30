from typing import List

import disnake
from disnake.ui import *


class JustifyPaginatorInterface(disnake.ui.View):    

    def __init__(self, pages: List[str]):
        self.pages = pages
        self.current_index = 0
        super().__init__(timeout=None)


    @button(emoji="⏪")
    async def go_to_start(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        self.previous_page.disabled = True
        self.go_to_end.disabled = False
        
        if self.current_index == 0:
            self.go_to_start.disabled = True

        data = self.pages[0]
        await inter.response.edit_message(content=data, view=self)

    
    @button(emoji="◀️")
    async def previous_page(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        self.current_index -= 1
        data = self.pages[self.current_index]
        self.next_page.disabled = False
        self.previous_page.disabled = False

        if self.current_index == 0:
            self.go_to_start.disabled = True
            self.go_to_end.disabled = False
            self.previous_page.disabled = True
            self.next_page.disabled = False
        
        await inter.response.edit_message(view=self, content=data)

    @button(emoji="❌")
    async def stop_paginator(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await inter.delete_original_message()

        
    @button(emoji="▶️")
    async def next_page(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        self.current_index += 1
        data = self.pages[self.current_index]
        self.next_page.disabled = False
        self.previous_page.disabled = False

        if self.current_index == len(self.pages)-1:
            self.next_page.disabled = True
            self.go_to_end.disabled = True
        
        await inter.response.edit_message(view=self, content=data)
    
        
    @button(emoji="⏩")
    async def go_to_end(self, button: Button, inter: disnake.ApplicationCommandInteraction):
        self.go_to_start.disabled = False
        self.previous_page.disabled = False

        data = self.pages[-1]
        await inter.response.edit_message(content=data, view=self)
    