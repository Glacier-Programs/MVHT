from pygame import display, event, mouse
from pygame import QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame import quit as pgQuit
from pygame.time import Clock
from typing import NoReturn

from GUI.deeperElements import Button, AnimatedElement, Element, HoverElement
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
        print('Added: ', el)
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
            if hover.get_col():
                hover.on_hover()
                self.elements['hovering'].append(hover)
            elif hover in self.elements['hovering']:
                hover.on_off_hover()
    
    def _draw_screen(self) -> None:
        self.display.fill(BASICBACKGROUNDCOL)
        for key in self.elements:
            for el in self.elements[key]:
                el.render(self.display)
        display.flip()
