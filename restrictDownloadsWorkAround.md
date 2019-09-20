## Editing girder.local.cfg


   docker exec -it histomicstk_histomicstk bash
   cd girder/girder/conf
   nano girder.local.cfg
   ### This won't work because nano isn't installed!!
   sudo apt-get update
   sudo apt-get install nano
   nano girder.local.cfg
   
# Line to edit   
Find the part of the document that says this and change restrict_downloads to True

[histomicstk]
restrict_downloads = False

This option is set up to prevent users from downloading giant imaging data sets, but still allows a different set of permissions that allows them to at least browse


   
