from pygame import Surface
from pygame.font import Font, SysFont
from typing import Callable

from MVHT.Util.color import BLACK
from MVHT.Util.Global import get_var

'''
    Base classes for element functionality
    A lot of redudant metopds just to allow for overriding
'''

class Element:
    def __init__(self, coords : list[int], width : int, height : int, c : tuple[int]= BLACK) -> None:
        self.coords = coords
        self.width = width
        self.height = height
        self.c = c

        self.sprite = Surface((width, height))
        self.sprite.fill(c)
    
    def __str__(self) -> str:
        return 'Type: {}, Coords: {}, Size: {}, Color: {}, {}'.format(type(self), self.coords, self.size, self.c, self.get_extra_info())

    @property
    def size(self) ->  tuple[int, int]:
        return self.width, self.height
    
    def get_col(self) -> bool:
        mcoords : tuple[int] = get_var('mcoords')
        xcase : bool = (self.coords[0] < mcoords[0]) and (self.coords[0] + self.width > mcoords[0])
        ycase : bool = (self.coords[1] < mcoords[1]) and (self.coords[1] + self.height > mcoords[1])
        return xcase and ycase

    def get_extra_info(self) -> str:
        pass

    def render(self, surf : Surface) -> None:
        surf.blit(self.sprite, self.coords)

class Button(Element):
    def __init__(self, coords : list[int], width : int, height : int, c : tuple[int]=BLACK, on_click : Callable[[], None] = False) -> None:
        super().__init__(coords, width, height, c=c)
        if on_click:
            self.on_click = on_click
    
    def get_extra_info(self) -> str:
        return super().get_extra_info()

    def on_click(self):
        pass

class AnimatedElement(Element):
    def __init__(self, coords : list[int], width : int, height : int, c : tuple[int]=BLACK, stepped : bool=False) -> None:
        super().__init__(coords, width, height, c=c)
    
    def get_extra_info(self) -> str:
        return super().get_extra_info()

    def stepped_anim(self) -> None:
        # stepped animation (requires multiple frames)
        pass

    def on_anim(self) -> None:
        pass

class HoverElement(AnimatedElement):
    # an element that can be hovered over
    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = BLACK, stepped=False) -> None:
        super().__init__(coords, width, height, c=c, stepped=stepped)
        self.hoverSprite = Surface((width, height))
        self.hoverSprite.fill((255,255,255))
    
    def get_extra_info(self) -> str:
        return super().get_extra_info()

    def on_hover(self) -> None:
        pass

    def on_off_hover(self) -> None:
        pass

class Text(Element):
    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = BLACK) -> None:
        super().__init__(coords, width, height, c=c)
    
    @classmethod
    def make_font(cls, fontName : str, size : int, isSys = True) -> Font:
        if isSys:
            return SysFont(fontName, size)
        return Font(fontName, size)
