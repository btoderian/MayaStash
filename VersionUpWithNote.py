## Saves a new file in the current directory.  The version number and File Description will be updated automatically through this script.  Descriptions are optional! 
## You must follow this convention for naming your first file:
## FileName_v001_FileDescription
## This formatting will keep your files organized if sorted by time or name.

import os 
import maya.cmds as cmds

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
        
def versionUpWithNote():
    # Get the current file path
    file_path = cmds.file(q=True, sn=True)
    if not file_path:
        cmds.warning("Please save the file before using this script.")
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
    versionUpWithNote()
  
  
