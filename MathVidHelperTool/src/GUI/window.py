from pygame import display, event, mouse
from pygame import QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame import quit as pgQuit
from pygame.time import Clock
from typing import NoReturn

from GUI.deeperElements import Button, AnimatedElement, Element, HoverElement
from GUI.dropDown import DropdownPopup
from MVHT.Util.settings import BASICBACKGROUNDCOL, MAXFPS
from MVHT.Util import Global

class Window:
    def __init__(self, width : int, height : int, title : str) -> None:
        self.display = display.set_mode((width, height))
        display.set_caption(title)
        self.title = title
        self.elements = {'buttons' : [], 'static' : [], 'animated' : [], 'hover' : [], 'hovering' : []}
        self.CLOCK = Clock()

        Global.make_global('mcoords', (0,0))

    @property
    def size(self) -> tuple[int]:
        return self.display.get_size()

    @property
    def center(self) -> tuple[int]:
        size = self.size
        return [size[0]/2, size/2]

    def center_element(self, element : Element) -> tuple[int]:
        ''' return the coordinates needed to center an element on screen '''
        pass

    def add_element(self, el : Element) -> None:
        self._add_element(el)

    def remove_element(self, el : Element) -> None:
        self._remove_element(el)

    def on_close(self) -> None:
        ''' is meant to be overidden by subclasses '''
        pass

    def run(self) -> None:
        while True:
            self._loop()

    def _add_element(self, el : Element) -> None:
        if isinstance(el, Button):
            self.elements['buttons'].append(el)
        if isinstance(el, AnimatedElement):
            self.elements['animated'].append(el)
        if isinstance(el, HoverElement):
            self.elements['hover'].append(el)
        self.elements['static'].append(el)

    def _remove_element(self, el : Element) -> None:
        for key in self.elements:
            if el in self.elements[key]:
                self.elements[key].remove(el)

    def _shutdown(self) -> None:
        pgQuit()
        quit()

    def _loop(self) -> NoReturn:
        self._update()
        self._draw_screen()
        self.CLOCK.tick(MAXFPS)

    def _update(self) -> None:
        for ev in event.get():
            if ev.type == QUIT:
                self.on_close()
                self._shutdown()
            elif ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                Global.set_var('mcoords', mouse.get_pos())
                for btn in self.elements['buttons']:
                    if btn.get_col():
                        btn.on_click()

        Global.set_var('mcoords', mouse.get_pos())
        for hover in self.elements['hover']:
            intersect = hover.get_col()
            if intersect and not hover in self.elements['hovering']: # they interesct but arent already in the list
                hover.on_hover()
                self.elements['hovering'].append(hover)
            elif not intersect and hover in self.elements['hovering']: # the exact opposite of the last if
                self.elements['hovering'].remove(hover) # remove it from list of hovered objects
                hover.on_off_hover() # apply event for when its no longer hovered
    
    def _draw_screen(self) -> None:
        self.display.fill(BASICBACKGROUNDCOL)
        for key in self.elements:
            for el in self.elements[key]:
                el.render(self.display)
        display.flip()
