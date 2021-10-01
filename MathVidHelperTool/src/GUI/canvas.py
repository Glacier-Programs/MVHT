from .deeperElements import Frame, Button, Element, AnimatedElement

class Canvas(Frame):
    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = ..., buts: list[Button] = ..., anims: list[AnimatedElement] = ..., static: list[Element] = ...) -> None:
        super().__init__(coords, width, height, c=c, buts=buts, anims=anims, static=static)
