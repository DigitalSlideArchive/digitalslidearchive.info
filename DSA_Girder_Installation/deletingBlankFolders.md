I accidentally created blankFolders when I had a script run that was helping me reorganize my slide data.  In this case, I created
7 folders for each patient and each possible stain that could have been done.  However many patients didn't have any slide(s) with stain X,
and so I wanted something to find empty folders and then prune them.

I did this using the girder python API.

  patientFolders = recurseGetResource(gc, FOLDER_ID, "folder", parentType='folder')

  for patientFolder in patientFolders:
      stainFolders = recurseGetResource(gc, patientFolder["_id"], "folder", parentType='folder')
    
      for stainFolder in stainFolders:
          items = list(gc.listItem(stainFolder["_id"]))
          if len(items) == 0:
              gc.delete("folder/" + stainFolder["_id"])
