import glob
import os
import pathlib
import subprocess

# List containing all files in folders and subfolders ordered by date created.
# From oldest to newest.
alldMDFilesPath = []

# Get path of current directory
workingDirPath = pathlib.Path().absolute()
# Get paths to subfolders in working directory.
subFoldersPath = [f.path for f in os.scandir(workingDirPath) if f.is_dir()]
# Oorder the subfolders by date created.
subFoldersPath.sort(key=os.path.getctime)

# Add file paths to a list. The files in the main folder/working directory are
# put together at the beginning. Then each folder.
# But first add the current folder/working directory.
# Path to find all .md files.
mainFolder = os.path.join(workingDirPath, "*.md")
# Get a list of the files in the folder.
MDfiles = glob.glob(mainFolder)
# Sort list by date created.
MDfiles.sort(key=os.path.getctime)
# Append files to master list.
alldMDFilesPath.extend(MDfiles)
# Now do the same for subfolders.
for dir in subFoldersPath:
    # Create path to .md files.
    subFolderFiles = os.path.join(dir, "*.md")
    # Get a list of the files in the folder.
    MDfiles = glob.glob(subFolderFiles)
    # Order files in subdolder by date. Then add them to the master list
    # together.
    MDfiles.sort(key=os.path.getctime)
    # Add files individually.
    alldMDFilesPath.extend(MDfiles)

# Check that last line in all files is an empty line or add an empty line if
# needed.
for filePath in alldMDFilesPath:
    # Open file to read and write.
    file = open(filePath, "r+")
    # Get the last line of the file.
    lastLine = file.readlines()[-1]
    # Check if the last line is an empty line.
    # First assume last line is an empty line.
    emptyLine = True
    # Check every character in the last line.
    for char in lastLine:
        # Check character to see if it's just empty space.
        if char != " ":
            # If it's not an empty space, then it must be some character and
            # the line is not empty line and the emptyLine variable will now
            # reflect this. After the emptyLine variable has been set to False
            # for the last line of file, there is no way to make it say
            # otherwise for that file.
            emptyLine = False
    # If the emptyLine variable is false, then add an empty line to the file
    # and close the file.
    if emptyLine is False:
        file.write("\n")
        file.close()

# Create bash script to run pandoc command.
# First add all document paths to a single script.
# Variable to hold the string.
allPaths = " "
for filePath in alldMDFilesPath:
    allPaths += "'" + filePath + "' "

bashScriptName = "ConversionScript.sh"
# Create file.
bashScript = open(bashScriptName, "w")
# Pandoc command used. Broken for readability.
pandocCommand = (
    "pandoc -s -V documentclass=article -V fontsize=12pt -f "
    + "markdown+lists_without_preceding_blankline+hard_line_breaks "
    + "--toc --include-in-header FormattingSettings.tex -o output.pdf"
)
# The pandoc command with the file paths.
fullCommand = pandocCommand + allPaths

# Append full command to bash script.
bashScript.write(fullCommand)
bashScript.close()

# Run command. Change working directory as well.
process = subprocess.Popen(
    fullCommand, stdout=subprocess.PIPE, cwd=workingDirPath, shell=True
)
# Get output messages.
output, error = process.communicate()
