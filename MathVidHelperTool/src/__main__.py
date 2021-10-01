from MVHT.Util import Global, color

import GUI
from GUI.deeperElements import *
from GUI.dropDown import *

def _create_elements():
    WINSIZE = Global.get_var('WINDOW').size
    
    FONT = Text.make_font('arial', 20)
    Global.make_global('FONT',FONT)

    topFrame = Frame([0,0], WINSIZE[0], 25, c=color.GREY)

    redBtn = Button([0,0], 75, 25, c=(255,0,0), on_click=lambda : print('clicked red button'))

    projectMenu = DropdownMenu([0,0], 75, 25, c=(177,177,177), title='Project', font=Global.get_var('FONT'))
    physicsMenu = DropdownMenu([100,0], 75, 25, c=(177,177,177), title='Physics', font=Global.get_var('FONT'))
    mathMenu = DropdownMenu([200,0], 75, 25, c=(177,177,177), title='Math', font=Global.get_var('FONT'))
    variableMenu = DropdownMenu([300,0], 75, 25, c=(177,177,177), title='Variables', font=Global.get_var('FONT'))
    extensionsMenu = DropdownMenu([400,0], 75, 25, c=(177,177,177), title='Extensions', font=Global.get_var('FONT'))

    projectMenu.popUp.add_option('New', Global.get_var('FONT'), lambda : print('clicked red button'))

    topFrame.add_element(projectMenu)
    topFrame.add_element(physicsMenu)
    topFrame.add_element(mathMenu)
    topFrame.add_element(variableMenu)
    topFrame.add_element(extensionsMenu)

    Global.get_var('WINDOW').add_element(topFrame)
    Global.make_global('TOPFRAME',topFrame)

def main():
    # start stuff
    win = GUI.Window(1000, 800, 'MVHT')
    Global.make_global('WINDOW', win)

    _create_elements()

    win.run()

if __name__ == '__main__':
    main()