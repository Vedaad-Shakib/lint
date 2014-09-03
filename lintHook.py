# author Vedaad Shakib
# NOTE: this is meant to be a git hook i.e. it is in the directory .git/hooks, therefore it will check the files in ../..

import re
import os

nameOfFolder = "Lint" # the name of the repository

def lint(file):
    global nameOfFolder
    lineNum = 0
    commentNum = 0

    # variables to track multiline comments
    javadocCommentStart = 0
    javadocCommentActive = False;

    # gets filename from absolute path
    fileName = os.path.relpath(file.name, nameOfFolder).replace("..", nameOfFolder)
    
    for line in file:
        if len(line.strip()) == 0: continue; # continue if there is nothing in the line
        lineNum += 1
        # strips off whitespace and checks if the bracket is on its own line.
        if "/" in line: # if there is a comment
            if line[:line.strip().index("/")].strip() == "{": # get rid of the part with the comments
                print fileName +   " has an isolated bracket on line " + str(lineNum)
        else:
            if line.strip() == "{": 
                print fileName + " has an isolated bracket on line " + str(lineNum)
                
        checkVar = re.findall("\S=\S", line) #matches [not space]=[not space]
        if checkVar:
            print fileName + " has squished operators on line " + str(lineNum)

        # check for comments
        if "//" in line:
            commentNum += 1
        if "/*"in line:
            javadocCommentStart = lineNum
            javadocCommentActive = True
        if line.strip()[-2:] == "*/":
            javadocCommentActive = False
            commentNum += (lineNum - javadocCommentStart + 1)

    if commentNum < lineNum/10: # checks if there is an adequate number of comments in the file
        print fileName + " has " + str(commentNum) + " comments. You need a minimum of " + str(lineNum / 10) + " comments to explain your work"

# recursively returns absolute paths in a directory and its subdirectories
def absolutePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           if f[f.index("."):] == ".txt":
               yield os.path.abspath(os.path.join(dirpath, f))
           
def main(path):
    fileGenerator = absolutePaths(path)
    for i in fileGenerator:
        lint(open(i))
        
dirname = os.path.dirname(os.path.abspath("lint.py")) # meant to be a git hook i.e. it is in the directory .git/hooks, therefore it will check the files in ../..
main(dirname)

