from typing import Callable

from MVHT.Util.Global import get_var
from MVHT.Util.settings import DEFAULTFONTCOLOR
from .element import *

class TextButton(Button):
    def __init__(self, coords: list[int], width: int, height: int, text : str, c: tuple[int] = ..., 
                 on_click: Callable[[], None] = False) -> None:
        super().__init__(coords, width, height, c=c, on_click=on_click)

class Frame(Button, HoverElement):
    # can contain buttons, so inherits from button in order to be considered clickable
    # same for inheriting HoverElement
    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = BLACK, buts: list[Button] = [],
                 anims: list[AnimatedElement] = [], static: list[Element] = []) -> None:
        super().__init__(coords, width, height, c=c)
        self.subs : dict[str,Element] = {'buttons' : buts, 'static' : static, 'animated' : anims, 'hover' : []}
    
    def on_click(self) -> None:
        for but in self.subs['buttons']:
            if but.get_col():
                but.on_click()

    def on_hover(self) -> None:
        for hov in self.subs['hover']:
            if hov.get_col():
                hov.on_hover()

    def add_element(self, element : Element) -> None:
        if isinstance(element, Button):
            self.subs['buttons'].append(element)
        if isinstance(element, AnimatedElement):
            self.subs['animated'].append(element)
        if isinstance(element, HoverElement):
            self.subs['hover'].append(element)
        self.subs['static'].append(element)
        self.post_to_sprite(element)
        print('added: ', element)

    def create_element(self, type, *args, **kwargs) -> None:
        # create an element directly in frame subelements dict
        # types : 'static', 'buttons', 'animated' 
        
        self.subs[type].append(Element(args, kwargs))

        self.post_to_sprite(self.subs [type] [len(self.subs[type])-1])

    def post_to_sprite(self, element : Element) -> None:
        self.sprite.blit(element.sprite, element.coords)
