from GUI.workpace import Workspace
from GUI.element import AnimatedElement, Button, Element, AnimatedElement

class ScriptWorkspace(Workspace):
    def __init__(self, coords: list[int], width: int, height: int,  fileName : str, c: tuple[int] = ..., **tags) -> None:
        super().__init__(coords, width, height, c=c, buts=[], anims=[], static=[], **tags)
        self.fileName : str = fileName
        self.sprite.fill((0,0,0))

wrkspcs = {'script' : ScriptWorkspace, 'scene' : Workspace, 'physics' : Workspace, 'variables' : Workspace}
