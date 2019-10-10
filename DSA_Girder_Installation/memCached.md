### Caching/Performance
The DSA can utilize a local cache to speed up image access; theres an internal cacheing mechanism built in, however we 
recommend using memcached.  Since the containers can't be stopped/restarted, we have memcached running on the SERVER itself, 
not within a docker container.

On an ubuntu system, this can be installed with

   sudo apt-get install memcached
   
 
