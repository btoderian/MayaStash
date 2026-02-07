## Maya 2024 Hotkey Version  ##
## In viewport: toggle Anim controls, but leaves locators, meshes, joints, and images planes alone. ##
## In graph editor: toggle tangent handles. ##

import maya.cmds as cmds
import maya.mel as mel

def toggle_nurbs_clean():
    panel = cmds.getPanel(underPointer=True) or cmds.getPanel(withFocus=True)
    if not panel:
        return

    panel_type = cmds.getPanel(typeOf=panel)

    # Viewport
    if panel_type == "modelPanel":
        # 1. Query all the states we want to preserve
        poly_val    = cmds.modelEditor(panel, q=True, polymeshes=True)
        joint_val   = cmds.modelEditor(panel, q=True, joints=True)
        locator_val = cmds.modelEditor(panel, q=True, locators=True)
        img_val     = cmds.modelEditor(panel, q=True, imagePlane=True)
        
        # 2. Toggle the NURBS Curves status
        nurbs_val = not cmds.modelEditor(panel, q=True, nurbsCurves=True)

        # 3. Apply settings
        # We use 'allObjects=False' to clear the deck, then explicitly enable what we want kept
        cmds.modelEditor(panel, e=True, allObjects=False)
        cmds.modelEditor(panel, e=True, 
                         nurbsCurves=nurbs_val, 
                         polymeshes=poly_val, 
                         joints=joint_val, 
                         locators=locator_val, 
                         imagePlane=img_val)
        return

    # Graph Editor (Logic remains the same)
    if panel_type == "scriptedPanel" and cmds.scriptedPanel(panel, q=True, type=True) == "graphEditor":
        if cmds.optionVar(q="graphEditorDisplayTangents") or cmds.optionVar(q="graphEditorDisplayActiveTangents"):
            mel.eval("GraphEditorNeverDisplayTangents")
        else:
            mel.eval("GraphEditorDisplayTangentActive")

        cmds.refresh(f=True)
        return

toggle_nurbs_clean()
