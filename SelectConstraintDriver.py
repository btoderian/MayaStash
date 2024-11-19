#Find the object driving constraint relationship.  

import maya.cmds as cmds

def selectConstraintDriver():
   conToNodes = []
   selObj = cmds.ls(sl=True)
   for obj in selObj:
       if "ConTo" in obj:
           conToNodes.append(obj)
   sourceObjects = []
   constraints = cmds.listRelatives(type="constraint")
   if constraints:
       for constraint in constraints:
           sourceObjects.extend(
               [
                   sourceObject
                   for sourceObject in cmds.listConnections(
                       constraint + ".target[*].targetParentMatrix", s=1
                   )
                   if (cmds.objExists(sourceObject) and sourceObject not in sourceObjects)
               ]
           )
   for node in conToNodes:
       constraints = cmds.listRelatives(cmds.listRelatives(node, parent=True), type="constraint")
       if constraints:
           for constraint in constraints:
               sourceObjects.extend(
                   [
                       sourceObject
                       for sourceObject in cmds.listConnections(
                           constraint + ".target[*].targetParentMatrix", s=1
                       )
                       if (cmds.objExists(sourceObject) and sourceObject not in sourceObjects)
                   ]
               )
   if sourceObjects:
       cmds.select(sourceObjects)

def main():
        selectConstraintDriver()
