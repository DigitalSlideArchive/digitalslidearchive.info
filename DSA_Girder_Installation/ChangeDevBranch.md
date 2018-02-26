In some cases, you may want to use the dockerized version of DSA but pull/test a feature that is on a branch.  In order to 
do this you need to login to the docker container and pull the appropriate branch.  As an example:

   cd /opt/Histomics_SRC/ansible
   docker exec -i -t histomicstk_histomicstk bash
   ## now I am in the histomicstk/DSA docker image
   
   ## in my case
   git checkout virtual-folders
   # then rebuild and reset the server..
