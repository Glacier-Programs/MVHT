from __future__ import annotations
from os import chdir, mkdir # change working directory / make new directory
from MVHT.Project.MVHT_file_reader import MVHTFileReader

from MVHT.Util.settings import DEFAULTPROJECTSDIRECTORY

'''
<Project-Folder>
| Project File (main.mvht):
| | project info
| | extensions list
|
| Extenstions 
| | 
|
| <Assets-Folder>:
| | assets.txt
| | | list of assets
| | | linked assets locations (str representation of path to asset)
| | Locally Stored Asset Files {png, jpg, pyimg, mp4, txt}
'''

EMPTYFILEFORMAT = '''meta-data{
/v:0.0.04
}

dependencies{
*std
}

packages{

#dependencies
*std

[std]{
*script
*scene
*physics
*variables

[script]{
/v:0.0.01
}

[scene]{
/v:0.0.01
}

[physics]{
/v:0.0.01
}

[variables]{
/v:0.0.01
}
}
}
'''

class Project:
    def __init__(self, mvhtFile: MVHTFileReader) -> None:
        self.name = mvhtFile.fileName
        self.deps = []
        for key in mvhtFile.headers['dependencies'].vars:
            self.deps.append(mvhtFile.headers['depdendancies'].vars[key])
        for key in mvhtFile.headers['packages'].packages:
            for dep in mvhtFile.headers['packages'].packages[key].packages:
                self.deps.append(dep)
        print(self.deps)

    @classmethod
    def create_project(cls, name : str, path : str = None, **tags) -> Project:
        # tags has no functionality as of now
        # make project files and update projects list
        assignPath = True # whether or not to declare path in projects list

        # find path
        if not path: 
            assignPath = False
            path = DEFAULTPROJECTSDIRECTORY

        # create files
        chdir(path) # set cwd to proper location
        mkdir(name)
        mainFile = open(name + '/project.mvht', 'w') # create main project data file
        mainFile.write(EMPTYFILEFORMAT)
        mainFile.close()
        mkdir(name+'/assets')
        assestList = open(name+'/assets/assets.txt', 'w')
        assestList.close()

        # update projects list
        with open(DEFAULTPROJECTSDIRECTORY+'/projects.txt', 'r+') as file:
            data = file.read()
            data = data.split('\n')
            data[0] = int(data[0]) + 1
    
    @classmethod
    def load_project(cls, projName : str) -> Project:
        print('Loading: ', projName)
        with open(DEFAULTPROJECTSDIRECTORY+'/projects.txt') as file:
            for line in file.read().split('\n'):
                if line.split(':')[0] == projName and not line.split(':')[1]: # the project is in main directory
                    return Project(MVHTFileReader('/{}/project.mvht'.format(projName), DEFAULTPROJECTSDIRECTORY) )
