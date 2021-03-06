## Installation Guide for a Digital Slide Archive Instance

### Installation Requirements:

1) Root access  
2) Ubuntu 16.04 Machine (although very likely other platforms will work, testing coming as requested).  We have got this working on a Mac as well using Docker [ADD HREF]

### Further notes on Installation

All of the scripts needed for installation are available on the main HistomicsTK
website ( add git link).  We are using Dockerized containers which should make
simpler and faster.  Thism won't require building the entire software stack,
as they are prebuilt when you pull them from Docker Hub.  

### Step 1

We recommend upgrading the system.

```sudo apt-get update && sudo apt-get upgrade```

I created a default username (dsaadmin) during my initial installation with sudo access.  You can use whatever user you want, but they will need sudo access to get things properly configured.


```
bash  # My distro for some reason doesn't run BASH on startup for new users..
sudo useradd dsaadmin
sudo passwd dsaadmin
##Type in a password for the dsaadmin user
sudo usermod -a -G sudo dsaadmin```

![](assets/DSA_Installation-a6ce7.png)

You then want to logout and log in as the dsaadmin usermod

*** Optional/Bug Fix ***
For some reason, when I create the user as above, it is not creating creating a home directory, and it's also not making bash the default login shell.  

What I have done is run mkhomedir_helper so it creates my home directory.  I've also had to go in and edit /etc/passwd and amend it so it has the dsaadmin user default to running bash; originally it just said /home/dsaadmin: (i.e. nothing after the colon)

![](assets/DSA_Installation-2a655.png)
![](assets/DSA_Installation-f74da.png)

### Step 2
Install Docker:  These instructions assume your using Ubuntu 16.04.
Instructions have been modified to note the docker-ce installation, as apparently the docker version in Ubuntu 16.04 is now old

Directors for Docker were from here:
https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce
```bash
sudo apt-get install apt-transport-https \
    ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"
sudo apt-get update
sudo apt-get install docker-ce


sudo apt-get install  python-pip build-essential libssl-dev libffi-dev python-dev
sudo pip install --upgrade pip
```

### Now that we have pip, need to install docker-py and ansible into user space
```bash
pip install docker-py ansible --user
```

## Please note, you need to be a member of the docker group in order to check the status of docker containers; also you have to LOG OFF and then LOG BACK IN after adding the admin user to the docker group in order for the permissions to be properly updated.  If you forget this step, or forget to logout, you'll see something like below where it says cannot connect to docker daemon.

~~~
sudo usermod -a -G docker dsaadmin
logout
~~~

Check and see if docker is running...
~~~~
docker ps
~~~~
![](assets\DSA_Installation-7660f704.png)
![](assets\DSA_Installation-9bf6e7b7.png)

The docker containers are actually running, but the current user (dagutman) doesn't
have access to connect to the docker containers.  

~~~~
sudo usermod -a -G docker dsaadmin
exit
~~~~

Now Login again as dsaadmin and run the command
`docker ps`

### Now clone the Histomics Repo
We have opt'ed (pun intended) to install the Histomics/Girder installation into the /opt directory on our system
Please note it's important to make sure the dsaadmin user had the proper permissions to read/write into whatever
directories you create for these installation files

~~~~
cd /opt
sudo mkdir /opt/Histomics_Src
sudo chown dsaadmin:dsaadmin Histomics_Src

#now clone the repo
git clone https://github.com/DigitalSlideArchive/HistomicsTK.git Histomics_Src/

cd Histomics_Src
cd ansible
~~~~

To get information on how to install Histomics, there's a deploy_docker.py in the
ansible directory.  This helper script allows you to pull the latest histomicsTK images, and stop and start all the associated docker containers

~~~~
python deploy_docker.py --help
~~~~
![](assets/DSA_Installation-f8c4c.png)

#### Actually pull the docker containers
~~~~
python deploy_docker.py pull
~~~~

### Starting DSA for the first time

Once the images are pulled, you can simply Type
~~~~
python deploy_docker.py start
~~~~
![](assets/DSA_Installation-e09fa.png)


If you connect to http://localhost:8080 or http://myserver:8080 you can now start and browse.... however keep reading..

# Where's my stuff being stored??
So by default, when you start a new DSA/Girder instance it will create the following directories.

assetstore -> Where girder stores items/files/"stuff" that I've uploaded  
db -> where the mongoDB lives; mongo is running in a container so it needs to have a persistent location where the data is stored and can be backed up  
logs -> logs/errors/etc. get placed here

![](assets/DSA_Installation-40f14.png)

So I prefer to specify where the logs, Mongo database, and assetstores (storage space the DSA uses for files/items) live on my file system.  By default it will create all of this for you in

~/.histomicstk so in our case if I look in
/home/dsaadmin/.histomicstk

The Mongo Database should be stored in a directory outside of the actual docker
container, as an example I am storing it in /opt/MongoLocal


## Create a directory for Mongo

```sudo mkdir /opt/MongoLocal
sudo chown dsaadmin /opt/MongoLocal
mkdir /opt/MongoLocal/girder_db```

## The log directories will be stored in /opt/HistomicsData/logs which contains useful info  for debugging

~~~
sudo mkdir /opt/HistomicsData
sudo chmod g+s /opt/HistomicsData
sudo chown dsaadmin /opt/HistomicsData
~~~

## Create assetstore directory

```
sudo mkdir /opt/LocalAssetstore  
sudo chown dsaadmin /opt/LocalAssetstore
mkdir /opt/LocalAssetstore/girderAssetStore  ```


### Default User and password
on initial creation, the userid=admin and password=password
Obviously, this is not very secure.  So we <i>strongly</i> recommend you change this as follows

However, when you do this, you must also specify the user ID and password when
you do any upgrades to the main docker image.

![](assets/DSA_Installation-617a3.png)

### Startup script examples



## Creating a start up script
So in my use case, I am overriding the default directories girder tries to put "stuff";  so I wrote a one line bash script that will start the DSA, so below is the simplest script, I am calling it docker_local_start.sh and placing it on /opt/HistomicsSrc/ansible

    python deploy_docker.py start --db=/opt/MongoLocal/girder_db --assetstore=/opt/LocalAssetstore/girderAssetStore --logs=/opt/HistomicsData/logs


## Stopping/starting/updating docker

So I had already started my DSA instance before, but was using the default locations; so first thing I need to do is stop the version that's running.

~~~~~
python deploy_docker.py stop
python deploy_docker.py rm
~~~~~

![](assets/DSA_Installation-9d170.png)

Please note, I am also doing rm in this case; since I am going to now modify the files/locations/etc. that the program uses to store everything, I need to remove the docker container and have the ansible/deploy_docker script rebuild a working DSA version with the new file locations... this is fortunately simple...


![](assets/DSA_Installation-be105.png)

I used my favorite text editor (nano) to create the docker_local_start.sh file, and pasted in the command above... now all I need to do is


~~~~~
bash docker_local_start.sh
~~~~~

So here's what happens when something goes wrong...
![](assets/DSA_Installation-b1b9e.png)

It's a simple problem, It's complaining it can/t write to /opt/Histomics_Data  ... as it turns out above we created /opt/Histomics_DATA  (i.e. I goofed the capitalization).

## Another start up issue.. again I goofed up the paths

![](assets/DSA_Installation-2b855.png)




So to clean things up, I did.

~~~~~
python deploy_docker.py rm
bash docker_local_start.sh
~~~~~

![](assets/DSA_Installation-ee033.png)

In this case, I forgot to set the permissions as rw for the logs, so got a similar issue.  I changed the permission of /opt/Histomics_Data but forgot to set it for the logs subdirectory.

![](assets/DSA_Installation-7a0a3.png)




If it works, you should see something like below:

![](assets/DSA_Installation-cf5f4.png)

Apparently two of the containers had started during my previous failed attempt, so to be safe, I am removing them so we are at a clean starting point.  Once it gets to the DSA container, you'll see a string of text/startup messages...

![](assets/DSA_Installation-3618b.png)

Which ideally should then produce something like the above image..i.e. lots of 'ok's


## So now the good part, it's running on my server on port 8080

![](assets/DSA_Installation-8aa23.png)

And if I peek in the directories, I can see that the logs were created, and so we seem to be off to a good start...

![](assets/DSA_Installation-451f9.png)




### Another sample docker_local_start.sh script

This one mounts a couple of more directories, and also prompts for the user
to enter a password if they overwrote the default password


    python deploy_docker.py start --retry --password= --db=/opt/MONGO_LOCAL/girder_db --assetstore=/opt/LOCAL_ASSETSTORE/girderAssetStore1 --logs=/opt/Histomics_DATA/logs --port=8080 -e /SLIDES:BOHR_SLIDES:ro  -e /TCGA_MIRROR:TCGA_MIRROR:ro  -e /opt/LOCAL_ASSETSTORE/SRC_GLOBAL_SCRATCH/DCM_STORAGE:LOCAL_DCM_STORAGE:rw

# Mounting File Systems within a docker container

So since we are using docker containers, the actual machine running the DSA/girder
software has it's own file system which is separate from the host operating system.

So by default, when you upload a file to the DSA, the files get stored in the assetstore
you specify when you fire up the Histomics/DSA container

However Girder also allows you to Import images.  In this case, the images / files
still reside on the original file system but are indexed in Girder.  This can have
a number of advantages as we leave the original files untouched.  This made it easier
for me to backup my slide files and also useful for testing.  


##### TO DO
Viewing Label Images  **WARNING**
Experimental-- view macro images

connect to the docker container

cd plugins
cd large_image
git branch -a
git checkout show-label-images

Should be embedded to make this work in the tag
{"images": ["macro", "label"]}

![](assets/DSA_Installation-c8460.png)


![](assets/DSA_Installation-c8460.png)


## Ubuntu 14.04 Notes

Please note on Ubuntu 14.04 it's docker not docker.io
I also upgraded pip after installing it, as it indicated I was using an older
version.
