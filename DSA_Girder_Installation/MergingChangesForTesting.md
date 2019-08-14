## Merging commits into a docker container  

In the case that new features have been added to girder/dsa but are not yet merged into the current docker image, here's what you can do.

### Login to Girder Container

1. Assuming your already logged into the server running the DSA instance

In this example, I want to pull a new feature in the dicom_viewer plugin.

```docker exec -it histomicstk_histomicstk bash
   cd plugins
   cd dicom_viewers
   git branch -a ## To double check I get the name of the branch
   git checkout test ## Create local branch
   git pull
   git merge 2.x-maintenance 
   git merge origin/archive-access
   ## This will remind me to add in github info.. I just make stuff up since I don't want to commit anything
   git config --global user.email "fakeuser@idontexist.com"
   git config --global user.name "Fake User"
   git merge origin/archive-access```

   
Most likely, this will cause vim to pop up, type Esc-w and then Esc-q  
