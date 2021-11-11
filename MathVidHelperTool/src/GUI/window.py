from pygame import display, event, mouse
from pygame import QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame import quit as pgQuit
from pygame.time import Clock
from typing import NoReturn

from GUI.deeperElements import Button, AnimatedElement, Element, Frame, HoverElement
from GUI.dropDown import DropdownPopup
from GUI.workpace import WorkspaceFrame
from MVHT.Util.settings import BASICBACKGROUNDCOL, MAXFPS
from MVHT.Util import Global

class Window:
    def __init__(self, width : int, height : int, title : str) -> None:
        self.display = display.set_mode((width, height))
        display.set_caption(title)
        self.title = title
        self.elements = {'buttons' : [], 'static' : [], 'animated' : [], 'hover' : [], 'hovering' : []}
        self.scoped_element = self
        self.CLOCK = Clock()

        Global.make_global('mcoords', (0,0))

    @property
    def size(self) -> tuple[int]:
        return self.display.get_size()

    @property
    def center(self) -> tuple[int]:
        size = self.size
        return [size[0]/2, size[1]/2]

    def center_element(self, element : Element) -> tuple[int]:
        ''' return the coordinates needed to center an element on screen '''
        center = self.center
        return [center[0]-element.width/2, center[1]-element.height/2]
        
    def add_element(self, el : Element, priority : bool = False) -> None:
        self._add_element(el, priority)

    def remove_element(self, el : Element) -> None:
        self._remove_element(el)

    def push_message(self, msg : str) -> None:
        pass

    def on_close(self) -> None:
        ''' is meant to be overidden by subclasses '''
        pass

    def run(self) -> None:
        while True:
            self._loop()

    def set_scoped_element(self, el : Element) -> None:
        self.scoped_element = el

    def _add_element(self, el : Element, priority : bool) -> None:
        if isinstance(el, Button) and not priority:
            self.elements['buttons'].append(el)
        elif isinstance(el, Button) and priority:
            self.elements['buttons'].insert(0, el)
        
        if isinstance(el, AnimatedElement) and not priority:
            self.elements['animated'].append(el)
        elif isinstance(el, AnimatedElement) and priority:
            self.elements['animated'].insert(0, el)

        if isinstance(el, HoverElement) and not 'no_hover' in el.tags and not priority:
            self.elements['hover'].append(el)
        elif isinstance(el, HoverElement) and priority and not 'no_hover' in el.tags:
            self.elements['hover'].insert(0, el)

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
            elif ev.type == KEYDOWN:
                if ev.unicode == 'p':
                    print(self.elements)
                self.scoped_element.push_message(ev.unicode)
            elif ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                Global.set_var('mcoords', mouse.get_pos())
                for btn in self.elements['buttons']:
                    if btn.get_col(Global.get_var('mcoords')):
                        btn.on_click(Global.get_var('mcoords'))
                        self.scoped_element = btn
                        if isinstance(btn, Frame):
                            self.scoped_element = btn.get_pressed_sub(Global.get_var('mcoords'))
                        break # originally meant to only press one button at a time. Now it has the bonus effect of stopping an infinite loop

        Global.set_var('mcoords', mouse.get_pos())
        for hover in self.elements['hover']:
            intersect = hover.get_col(Global.get_var('mcoords'))
            if intersect and not hover in self.elements['hovering']: # they interesct but arent already in the list
                hover.on_hover(Global.get_var('mcoords'))
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
