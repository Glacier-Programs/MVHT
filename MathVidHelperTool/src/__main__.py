from MVHT.Project.project import Project
from MVHT.Util import Global, color

import GUI
from GUI.workpace import *
from GUI.deeperElements import *
from GUI.dropDown import *

import popups
import cust_workspaces

def cancel_pop_up_decorator(popUp : Popup) -> None:
    ''' lowers the previous popup before popping up a new one'''
    if Global.get_var('popup'):
        Global.get_var('popup').pop_down()
    Global.set_var('popup', popUp)
    Global.get_var('popup').pop_up()

def _create_drop_downs() -> None:
    WINSIZE = Global.get_var('WINDOW').size

    topFrame = Frame([0,0], WINSIZE[0], 25, c=color.GREY)

    # make all drop downs
    projectMenu = DropdownMenu([0,0], 75, 25, c=(177,177,177), title='Project', font=Global.get_var('FONT'))
    physicsMenu = DropdownMenu([100,0], 75, 25, c=(177,177,177), title='Physics', font=Global.get_var('FONT'))
    mathMenu = DropdownMenu([200,0], 75, 25, c=(177,177,177), title='Math', font=Global.get_var('FONT'))
    variableMenu = DropdownMenu([300,0], 75, 25, c=(177,177,177), title='Variables', font=Global.get_var('FONT'))
    extensionsMenu = DropdownMenu([400,0], 80, 25, c=(177,177,177), title='Extensions', font=Global.get_var('FONT'))
    
    # projects
    projectMenu.popUp.add_option('New', Global.get_var('FONT'), popups.create_new_project_pop_up().pop_up)
    projectMenu.popUp.add_option('Load', Global.get_var('FONT'), popups.load_project_pop_up().pop_up)
    projectMenu.popUp.add_option('Save', Global.get_var('FONT'), lambda : print('clicked Save Project'))
    
    # physics
    physicsMenu.popUp.add_option('New System', Global.get_var('FONT'), lambda : print('clicked New Physics System'))
    physicsMenu.popUp.add_option('New', Global.get_var('FONT'), lambda : print(str(physicsMenu.popUp)))

    # math
    mathMenu.popUp.add_option('New', Global.get_var('FONT'), lambda : print('clicked New Project'))

    topFrame.add_element(projectMenu)
    topFrame.add_element(physicsMenu)
    topFrame.add_element(mathMenu)
    topFrame.add_element(variableMenu)
    topFrame.add_element(extensionsMenu)

    Global.get_var('WINDOW').add_element(topFrame)
    Global.make_global('TOPFRAME',topFrame)

def _create_elements() -> None:
    WINSIZE = Global.get_var('WINDOW').size
    _create_drop_downs()
    WorkspaceFrame.set_workspaces(cust_workspaces.wrkspcs)
    work_space_frame = WorkspaceFrame([0,25], WINSIZE[0]/2, 500, c = color.BLUE, no_hover=True)
    Global.set_var('workspace-frame', work_space_frame)
    Global.get_var('WINDOW').add_element(work_space_frame)

def _make_variables() -> None:
    Global.make_global('popup', None)
    Global.make_global('workspace-frame', None)
    Global.make_global('FONT',Text.make_font('arial', 20))
    Global.make_global('project',None,on_change=lambda: get_var('workspace-frame').change_project(get_var('project')))

def _start_up() -> None:
    _make_variables()
    _create_elements()

def main():
    # start stuff
    win = GUI.Window(1000, 800, 'MVHT')
    Global.make_global('WINDOW', win)
    _start_up()

    win.run()

if __name__ == '__main__':
    main()
