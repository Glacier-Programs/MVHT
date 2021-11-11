'''
Issues / To Fix:
- tab buttons on workspace frame don't hold proper values for opening workspaces
- after clicking on a tab, workspace becomes extremely bugged and doesn't allow for rendering
'''

from pygame import Surface
from GUI.element import AnimatedElement, Button, Element
from MVHT.Project.project import Project
from MVHT.Util.Global import get_var, set_var
from MVHT.Util.color import BLACK, BLUE, DARKGREY, GREY, WHITE
from .deeperElements import Frame, TextButton

class Workspace(Frame):
    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = ..., buts: list[Button]=[],
                 anims: list[AnimatedElement]=[], static: list[Element] = [], **tags) -> None:
        super().__init__(coords, width, height, c=c, buts=buts, anims=anims, static=static)
        self.active = False

    def _set_active(self) -> None:
        ''' sets element to Window.scoped_element. required whenever clicked on '''
        self.active = True
        get_var('WINDOW').scoped_element = self

    def on_click(self, coords: tuple[int]) -> None:
        self._set_active()

    def on_off_click(self, coords : tuple[int]) -> None:
        self.active = False
    
    def recieve_text(self, text : str) -> None:
        pass

class WorkspaceFrame(Frame):
    wrkspcs = {'filler' : None}

    def __init__(self, coords: list[int], width: int, height: int, c: tuple[int] = ..., **tags) -> None:
        super().__init__(coords, width, height, c=c, anims=[], buts=[], static=[], **tags)
        self.tabs = []
        self.tabs_frame = Frame([0,0], width, 25, c=WHITE, buts=[], anims=[], static=[])
        self.active_workspace = Workspace([0,25], width, height-25,c=BLUE)

    def on_click(self, mcoords : list[int]) -> None:
        if mcoords[1] < 25 + self.height:
            print('clickety clickety on tabs')
            self.tabs_frame.on_click([mcoords[0]-self.coords[0], mcoords[1]-self.coords[1]])
        else:
            self.active_workspace.on_click([mcoords[0]-self.coords[0], mcoords[1]-self.coords[1]])
    
    def render(self, surf: Surface) -> None:
        self.tabs_frame.render(self.sprite)
        self.active_workspace.render(self.sprite)
        return super().render(surf)

    def change_project(self, proj : Project) -> None:
        if proj == None:
            return
        self.tabs_frame.flush()
        self.tabs = []
        counter = 0
        for dep in proj.deps:
            if not dep in WorkspaceFrame.wrkspcs:
                raise TypeError('Project Error: No Workspace Defined for Dependancy {} in Project {}'.format(dep, proj.name))
            self.tabs.append(TextButton([counter*75+counter*10,0], 75, 25, dep, get_var('FONT'), c=WHITE, fc=BLACK, onClick=lambda: self._open_workspace( dep )))
            self.tabs_frame.add_element(self.tabs[counter])
            counter += 1
    
    def _open_workspace(self, dep : str) -> None:
        print(dep)
        self.load_workspace(WorkspaceFrame.wrkspcs[dep])

    def load_workspace(self, workspace : Workspace) -> None:
        self.active_workspace = workspace
    
    @classmethod
    def set_workspaces(cls, workspaces : dict[str : Workspace]) -> None:
        WorkspaceFrame.wrkspcs = workspaces
    
    @classmethod
    def add_workspace(cls, name : str, object : Workspace) -> None:
        WorkspaceFrame.wrkspcs[name] = object
