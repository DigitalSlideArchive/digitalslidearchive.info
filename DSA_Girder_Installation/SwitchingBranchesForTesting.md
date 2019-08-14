### Switching branches to test out new features


First you must ssh/connect to the main girder directory so normally this would be

   docker exec -it histomicstk_histomicstk bash
   
This will log into the dockerc container where you can switch branches

You should be in /opt/histomicstk/girder

We recommend creating a test branch, and then merging in whatever fixes, branches together.  I am also configuring
a fake email name, as I never actually want to commit from within a docker image, but it will complain otherwise


    
    git pull
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
    git checkout -b test  
    #git merge <branchname>
    git merge origin/archive-access
    ## Have to use VIM to write comments about the merge..  <Esc>:w <Esc>:q 
    girder-install web --dev
    
If you added a plugin, don't forget to aso ENABLE it in the Admin Panel


### Using Memcached

Create a config file in the directory you start girder from.. usually /opt/HistomicsTK_SRC/ansible or similar;  
the config file 

cat setup.cfg 
[large_image]
cache_memcached_url: ["dockerhost"]

You should hopefully see something in the Girder Logs that mentions its using MEMCACHED instead of Python for cacheing

