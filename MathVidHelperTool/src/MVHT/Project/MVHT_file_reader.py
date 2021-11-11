from __future__ import annotations

'''
I already defined how the file stuff works in the readme and i dont feel like redoing it
Just go there to see how the files work. Here's an example file for fun:

header{
*package1
*package2
[package1]{
/a:1
/b:3
/c:a+b
}
[package2]{
#package1   (this is a comment. '#' imports values from another package or header in scope)
#package1.c (only take 'c' from 'package')
/d:3-c
}
}

'''

class Package:
    def __init__(self, packages : dict[str:Package], vars : dict[str:any]) -> None:
        self.packages = packages
        self.vars = vars

    def get_all_packages(self) -> list[Package]:
        alist = []
        for pack in self.packages:
            alist += self.packages[pack].get_all_packages
        return alist


class Header:
    def __init__(self, headers : dict[str:Header], packages : dict[str:Package], vars : dict[str:any]) -> None:
        self.headers = headers
        self.packages = packages
        self.vars = vars

class MVHTFileReader(Header):
    '''
    Special class for reading an MVHT file
    '''
    def __init__(self, fileName : str, path : str = '') -> None:
        self.headers = {}
        self.fileName =fileName
        self.path = path
        # complete a set of curly braces before going on
        with open(path+fileName) as file:
            data = file.read().split('\n')
            package_depth : list[Package, Header]= [] # for when accessing nested packages.
            for line in data:
                # cleaning up the code
                if '(' in line: line = remove_comments(line) # remove comments
                if line == '': line += ' ' # solve index issues
                
                # actually reading the line
                if line == '}': # end of code block
                    package_depth.pop(0)
                elif line[0] == '/': # variable
                    sides = line.split(':')
                    package_depth[0].vars[sides[0][1:len(sides[0])]] = sides[1] # needed to be so complicated to allow for 1 char vars
                elif line[0] == '.': # make an unassigned value
                    pass
                elif line[0] == '*': # instantiate package
                    package_depth[0].packages[line[1:]] = Package({},{})
                elif line[0] == '[': # define package
                    package_depth.insert(0, package_depth[0].packages[line[1:-2]])
                elif line[0] == '#': # import from other header
                    pass
                elif line != ' ': # define header
                    self.headers[line[:-1]] = Header({}, {}, {})
                    package_depth.insert(0, self.headers[line[:-1]])
    
    def get_packages(self) -> list[Package]:
        alist = []
        for key in self.headers:
            for package in self.headers[key].package:
                alist += self.headers[key].packages[package].get_all_packages()

def remove_comments(line : str) -> str:
    in_comment = False
    returnMe = ''
    for char in line:
        if char == '(':
            in_comment = True
            continue
        if char == ')' and in_comment:
            in_comment = False
            continue
        if in_comment:
            continue
        returnMe += char
    return returnMe
