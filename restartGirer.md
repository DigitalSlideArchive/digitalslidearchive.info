### How to restart Girder Server

#Access the main dsa container

docker exec -it histomicstk_histomicstk bash





touch /opt/girder/girder/conf/girder.dist.cfg 

## how to restart/rebuild the server

girder build --dev
