from pygame import Surface
from pygame.font import Font
from typing import Callable

from .deeperElements import Frame, AnimatedElement, Element, Button, TextButton

from MVHT.Util.Global import get_var
from MVHT.Util.settings import DEFAULTFONTCOLOR
from MVHT.Util.color import BLACK

class DropdownMenu(Frame, AnimatedElement):
    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = BLACK, buts: list[Button] = [], 
                 anims: list[AnimatedElement] = [], static: list[Element] = [], title : str = '', font : Font = False) -> None:
        super().__init__(coords, width, height, c=c, buts=buts, anims=anims, static=static)
        self.steps : int= 0
        self.maxSteps : int = 2 # length of animation in seconds
        
        self.popUp = DropdownPopup(self, c=c)
        self.poppedOut = False

        if font:
            self.sprite.blit(font.render(title, True, DEFAULTFONTCOLOR), (0,0))
    
    def on_element_add(self) -> None:
        addedEl : Element = self.subs[len(self.subs)-1]
        widths : int = 0
        for el in self.subs:
            if addedEl == el:
                break
            widths += el.width
        addedEl.coords[0] = widths

    def on_hover(self, mcoords : tuple[int]) -> None:
        self.on_anim()
        if not self.poppedOut:
            self.popUp.pop_up()
            self.poppedOut = True

    def on_off_hover(self) -> None:
        self.steps = 0
        self.poppedOut = False
        self.popUp.pop_down()
    
    def on_anim(self) -> None:
        dTime : float = get_var('WINDOW').CLOCK.get_time()


class DropdownPopup(Frame):
    def __init__(self, parent : DropdownMenu, c : tuple[int] = BLACK) -> None:
        self.parent = parent
        super().__init__([parent.coords[0], parent.coords[1] + parent.height], parent.width, 0, c=c, anims=[], static=[], buts=[]) # lists need to be made since super() otherwise makes self.subs the same for all subclasses

    def get_extra_info(self) -> str:
        return 'Option-Count: {}'.format(len(self.subs['buttons']))

    def get_col(self, mcoords : tuple[int]) -> None:
        return self.parent.get_col(mcoords) or super().get_col(mcoords)

    def add_option(self, name : str, font : Font, onClick : Callable) -> None:
        if len(name) * 10 > self.width:
            self.width = len(name) * 10
        self.height += 25
        self.update_size()
        btn = TextButton([0, len(self.subs['buttons']) * 25], self.width, 25, name, font, onClick=onClick, c=self.c)
        self.add_element(btn)

    def on_off_hover(self) -> None:
        self.parent.on_off_hover()
        self.pop_down()

    def update_size(self) -> None:
        newsprite = Surface((self.width, self.height))
        newsprite.blit(self.sprite, (0,0))
        self.sprite = newsprite

    def pop_up(self) -> None:
        get_var('WINDOW').add_element(self, priority = True)
    
    def pop_down(self) -> None:
        get_var('WINDOW').remove_element(self)
