## Saves a new file in the current directory.  The version number and File Description will be updated automatically through this script.  Descriptions are optional! 
## You must follow this convention for naming your first file:
## FileName_v001_OptionalDescription
## This formatting will keep your files organized if sorted by time or name.

## Use this python script to run or as a button:
## import MayaStash.VersionUpWithNote ; MayaStash.VersionUpWithNote.Save()

import os 
import maya.cmds as cmds
import re

def saveWithNote_getVersion(file_path):
    # Extract version number from file name
    pattern = r"_v(\d+)_"
    match = re.search(pattern, file_path)
    if match:
        version_number = int(match.group(1))
    else:
        version_number = 1
    return version_number

def saveWithNote_getUserNote():
    # Prompt the user to enter a user note
    user_note = cmds.promptDialog(
        title='User Note',
        message='Enter a user note:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )

    if user_note == 'OK':
        user_note_text = cmds.promptDialog(query=True, text=True)
        if not user_note_text:
            user_note_text = ""
        return user_note_text

    if user_note == 'Cancel':
        return
        
def Save():
    # Get the current file path
    file_path = cmds.file(q=True, sn=True)
    if not file_path:
        open_save_dialog()
        return

    if file_path:
        # Get the directory, project name, and shot details
        directory, file_name = os.path.split(file_path)
        project_name = os.path.basename(os.path.normpath(directory))
        shot_details = file_name.split("_v")[0]  # Assuming everything preceeding version number is correct

    # Get and increment the current version number with 3 digits
    version_number = str(int(saveWithNote_getVersion(file_name)) + 1).zfill(3)

    # Get user note
    user_note = saveWithNote_getUserNote()

    # Generate the new file name
    if user_note:
        new_file_name = "{}_v{}_{}.ma".format(shot_details, version_number, user_note)
    else:
        #Changing this so the script just stops on cancelling
        #new_file_name = "{}_v{}.ma".format(shot_details, version_number)
        return

    # Construct the new file path
    new_file_path = os.path.join(directory, new_file_name)

    # Save the file with the new file path
    cmds.file(rename=new_file_path)
    cmds.file(save=True, type="mayaAscii")

    # Feedback
    print("File saved as: {}".format(new_file_path))
    cmds.headsUpMessage("File saved as: {}".format(new_file_path), t=10)

if  __name__ == "__main__":
    Save()

def sSave():
    Save()
    cmds.headsUpMessage("SMoooooCH!", t= 0.3)

def open_save_dialog(suggested_name="FileName_v001_OptionalDescription.ma"):
    """
    Opens the Maya file save dialog with a suggested file name.
    """
    # Open Maya's file save dialog
    file_path = cmds.fileDialog2(
        fileMode=0,  # 0 for Save mode
        dialogStyle=2,  # Maya-style dialog
        caption="Save File As",
        startingDirectory=(cmds.workspace(query=True, directory=True)+suggested_name),
        fileFilter="Maya Files (*.ma *.mb)",
        okCaption="Save",
    )
    
    # Display the selected path (or save the file here if desired)
    if file_path:
        # Ensure the file path has the correct extension
        if not file_path[0].endswith((".ma", ".mb")):
            file_path[0] += ".ma"  # Default to `.ma` if no extension provided

        # Save the file
        cmds.file(rename=file_path[0])
        cmds.file(save=True, type="mayaAscii")
        print("File saved as:", file_path[0])
    else:
        print("No file saved.")
