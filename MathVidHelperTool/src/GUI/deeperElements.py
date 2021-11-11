from typing import Callable
from copy import deepcopy

from MVHT.Util.Global import get_var
from MVHT.Util.color import WHITE
from MVHT.Util.settings import DEFAULTFONTCOLOR
from .element import *

class TextButton(Button):
    def __init__(self, coords: list[int], width: int, height: int, text : str, font : Font, c: tuple[int] = BLACK, 
                 onClick: Callable[[], None] = False, fc: tuple[int] = WHITE, **tags) -> None:
        super().__init__(coords, width, height, c=c, onClick=onClick, **tags)
        self.fc = fc
        self.sprite.blit(font.render(text, True, fc), (0,0))
        
class Frame(Button, HoverElement):
    # can contain buttons, so inherits from button in order to be considered clickable
    # same for inheriting HoverElement
    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = BLACK, buts: list[Button] = [],
                 anims: list[AnimatedElement] = [], static: list[Element] = [], **tags) -> None:
        super().__init__(coords, width, height, c=c, **tags)
        self.subs : dict[str,Element] = {'buttons' : buts, 'static' : static, 'animated' : anims, 'hover' : []}

    def get_pressed_sub(self, mcoords : tuple[int]) -> Element:
        for but in self.subs['buttons']:
            if but.get_col([mcoords[0]-self.coords[0], mcoords[1]-self.coords[1]]):
                return but
        return self

    def on_click(self, coords : tuple[int]) -> None:
        for but in self.subs['buttons']:
            if but.get_col([coords[0]-self.coords[0], coords[1]-self.coords[1]]):
                but.on_click(get_var('mcoords'))

    def on_hover(self, mcoords : tuple[int]) -> None:
        for hov in self.subs['hover']:
            if hov.get_col([mcoords[0] - self.coords[0], mcoords[1] - self.coords[1]]):
                hov.on_hover([mcoords[0] - self.coords[0], mcoords[1] - self.coords[1]])

    def add_element(self, element : Element) -> None:
        if isinstance(element, Button):
            self.subs['buttons'].append(element)
        if isinstance(element, AnimatedElement):
            self.subs['animated'].append(element)
        if isinstance(element, HoverElement):
            self.subs['hover'].append(element)
        self.subs['static'].append(element)
        self.post_to_sprite(element)

    def flush(self) -> None:
        '''remove all sub elements'''
        for key in self.subs:
            for el in self.subs[key]:
                self.subs[key].remove(el)
                del(el)
            self.subs[key] = []

    def render(self, surf : Surface) -> None:
        for key in self.subs:
            for el in self.subs[key]:
                el.render(self.sprite)
        surf.blit(self.sprite, self.coords)

    def create_element(self, type, *args, **kwargs) -> None:
        # create an element directly in frame subelements dict
        # types : 'static', 'buttons', 'animated' 
        
        self.subs[type].append(Element(args, kwargs))

        self.post_to_sprite(self.subs [type] [len(self.subs[type])-1])

    def post_to_sprite(self, element : Element) -> None:
        self.sprite.blit(element.sprite, element.coords)

class Popup(Frame):
    def __init__(self, width: int, height: int, c: tuple[int] = BLACK, buts: list[Button] = [], 
                 anims: list[AnimatedElement] = [], static: list[Element] = [], **tags) -> None:
        super().__init__([0,0], width, height, c=c, buts=buts, anims=anims, static=static, **tags)
        self.coords = get_var('WINDOW').center_element(self)
    
    def pop_up(self) -> None:
        get_var('WINDOW').add_element(self, priority = True)

    def pop_down(self) -> None:
        get_var('WINDOW').remove_element(self)
        del(self)

class TextInput(Button):
    def __init__(self, coords: list[int], width: int, height: int, font : Font, fc : tuple[int] = WHITE, c: tuple[int] = BLACK, **tags) -> None:
        super().__init__(coords, width, height, c=c, **tags)
        self.font = font
        self.fc = fc
        self.active : bool = False
        self.response : str = ""
    
    def on_type(self, char : str) -> None:
        if self.active:
            self.response += char
    
    def on_click(self, mcoords: tuple[int]) -> None:
        self.active = True

    def get_response(self) -> str:
        return self.response

    def push_message(self, msg: str) -> None:
        if msg.encode() == b'\x08': # backspace
            self.response = self.response[:len(self.response)-1]
            return 
        self.response += msg
        return super().push_message(msg)

    def render(self, surf: Surface, **tags) -> None:
        self.sprite.fill(self.c)
        self.sprite.blit(self.font.render(self.response, True, self.fc), (0,0))
        surf.blit(self.sprite, self.coords)
