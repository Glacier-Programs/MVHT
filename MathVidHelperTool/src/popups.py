from GUI.deeperElements import Popup, TextButton, TextInput, Button
from GUI.element import Text
from MVHT.Util import color
from MVHT.Util import Global
from MVHT.Util.Global import get_var
from MVHT.Project.project import Project
from MVHT.Util.settings import DEFAULTPROJECTSDIRECTORY

def create_new_project_pop_up():
    newProjectPopup = Popup(200, 100, color.DARKGREY, anims=[], static=[], buts=[])
    newProjectPopup.add_element(Text([5,25], 'Project Name: ', get_var('FONT'), (255,255,255)))
    nppti = TextInput([100, 25], 100, 25, get_var('FONT'), c=color.BLACK)
    newProjectPopup.add_element(nppti) # get project name
    crt_new_proj_btn = TextButton([5, 50], 50, 25, 'Create', get_var('FONT'))
    def create_new_proj(mcoords : tuple[int]):
        Project.create_project(nppti.get_response())
        newProjectPopup.pop_down()
    crt_new_proj_btn.on_click = create_new_proj
    newProjectPopup.add_element(crt_new_proj_btn)
    newProjectPopup.add_element(TextButton([75, 50], 50, 25, 'Cancel', get_var('FONT'), onClick=newProjectPopup.pop_down))
    return newProjectPopup

def load_project_pop_up():
    loadProjectPopup = Popup(200, 100, color.DARKGREY, anims=[], static=[], buts=[])
    loadProjectPopup.add_element(Button([190,0], 10, 10, c=color.RED, onClick=loadProjectPopup.pop_down) )
    loadProjectPopup.add_element(Text([5,10], 'Projects: ', get_var('FONT'), color.WHITE))
    with open(DEFAULTPROJECTSDIRECTORY+'/projects.txt', 'r') as proj_list:
        data = proj_list.read().split('\n')
        proj_count = int(data[0])
        for i in range(proj_count):
            line = data[i+1].split(':')
            if line[1] == '':
                # file in projects folder
                loadProjectPopup.add_element( TextButton([5, (i+1)*25 + 25], 195, 25, line[0], get_var('FONT'), onClick=lambda:Global.set_var('project', Project.load_project(line[0]))) ) 
    return loadProjectPopup
