from pygame import Surface
from pygame.font import Font, SysFont
from typing import Callable

from MVHT.Util.color import BLACK
from MVHT.Util.Global import get_var

'''
    Base classes for element functionality
    A lot of redudant metods just to allow for overriding
'''

class Element:
    def __init__(self, coords : list[int], width : int, height : int, c : tuple[int]= BLACK, **tags) -> None:
        self.coords = coords
        self.width = width
        self.height = height
        self.c = c
        self.tags = tags

        self.sprite = Surface((width, height))
        self.sprite.fill(c)
    
    def __str__(self) -> str:
        return 'Type: {}, Coords: {}, Size: {}, Color: {}, {}'.format(type(self), self.coords, self.size, self.c, self.get_extra_info())

    @property
    def size(self) ->  tuple[int, int]:
        return self.width, self.height
    
    def get_col(self, coords :tuple[int]) -> bool:
        xcase : bool = (self.coords[0] < coords[0]) and (self.coords[0] + self.width > coords[0])
        ycase : bool = (self.coords[1] < coords[1]) and (self.coords[1] + self.height > coords[1])
        return xcase and ycase

    def get_extra_info(self) -> str:
        pass

    def push_message(self, msg : str) -> None:
        pass

    def render(self, surf : Surface) -> None:
        surf.blit(self.sprite, self.coords)

class Button(Element):
    def __init__(self, coords : list[int], width : int, height : int, c : tuple[int]=BLACK, onClick : Callable[[], None] = False, **tags) -> None:
        super().__init__(coords, width, height, c=c, **tags)
        if onClick:
            self.onClick = onClick
    
    def get_extra_info(self) -> str:
        return super().get_extra_info()

    def on_click(self, mcoords : tuple[int]) -> None:
        if self.onClick:
            self.onClick()

class AnimatedElement(Element):
    def __init__(self, coords : list[int], width : int, height : int, c : tuple[int]=BLACK, stepped : bool=False, **tags) -> None:
        super().__init__(coords, width, height, c=c, **tags)
    
    def get_extra_info(self) -> str:
        return super().get_extra_info()

    def stepped_anim(self) -> None:
        # stepped animation (requires multiple frames)
        pass

    def on_anim(self) -> None:
        pass

class HoverElement(AnimatedElement):
    # an element that can be hovered over
    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = BLACK, stepped=False, **tags) -> None:
        super().__init__(coords, width, height, c=c, stepped=stepped, **tags)
        self.hoverSprite = Surface((width, height))
        self.hoverSprite.fill((255,255,255))
    
    def get_extra_info(self) -> str:
        return super().get_extra_info()

    def on_hover(self) -> None:
        pass

    def on_off_hover(self) -> None:
        pass

class Text(Element):
    def __init__(self, coords: list[int], text : str, font : Font, fc: tuple[int] = BLACK, **tags) -> None:
        self.text = text
        super().__init__(coords, 0, 0, c=fc, **tags)
        self.sprite = font.render(self.text, True, fc)
    
    def get_col(self) -> bool:
        ''' collision shouldn't be detected on text. This insures that'''
        return False
    
    @classmethod
    def make_font(cls, fontName : str, size : int, isSys = True) -> Font:
        if isSys:
            return SysFont(fontName, size)
        return Font(fontName, size)
