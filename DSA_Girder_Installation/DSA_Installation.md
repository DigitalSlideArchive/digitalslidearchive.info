## Installation Guide for a Digital Slide Archive Instance

### Installation Requirements:

1) Root access  
2) Ubuntu 16.04 Machine (although very likely other platworks will work, testing coming soon)

### Further notes on Installation

All of the scripts needed for installation are available on the main HistomicsTK
website ( add git link).  We are using Dockerized containers which should make
simpler and faster.  This won't require building the entire software stack,
as they are prebuilt when you pull them from Docker Hub.  

#### Step 1
We recommend upgrading the system  
  apt-get update && apt-get upgrade

I created a default username (dsaadmin) during my initial installation with sudo access.

~~~
usermod -a -G sudo dsaadmin
~~~

#### Step 2
Install Docker: Please note on Ubuntu 14.04 it's docker not docker.io
I also upgraded pip after installing it, as it indicated I was using an older
version.

~~~~
sudo apt-get install docker.io python-pip
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo pip install --upgrade pip
~~~~

### Now that we have pip, need to install docker-py and ansible into user space

~~~~
pip install docker-py ansible --user
~~~~

## Please note, you need to be a member of the docker group in order to check the status of docker containers; also you have to LOG OFF and then LOG BACK IN after adding the admin user to the docker group in order for the permissions to be properly updated

~~~
usermod -a -G docker dsaadmin
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
sudo mkdir /opt/Histomics_SRC

#now clone the repo
git clone https://github.com/DigitalSlideArchive/HistomicsTK.git Histomics_SRC/

cd Histomics_SRC
cd ansible
~~~~

To get information on how to install Histomics, there's a deploy_docker.py in the
ansible directory

~~~~
python deploy_docker.py --help
~~~~
![](assets\DSA_Installation-95e35e3f.png)assets/DSA_Installation-95e35.png

#### Actually pull the docker containers
~~~~
python deploy_docker.py pull
~~~~

The Mongo Database should be stored in a directory outside of the actual docker
container, as an example I am storing it in /opt/MONGO_LOCAL

sudo mkdir /opt/MONGO_LOCAL
sudo chown dgutman /opt/MONGO_LOCAL

## The log directories will be stored in /opt/Histomics_DATA/logs useful for debugging

~~~
sudo mkdir /opt/Histomics_DATA
sudo chmod g+s /opt/Histomics_DATA
sudo chown dsaadmin /opt/Histomics_DATA
~~~

## Create assetstore directory

~~~
sudo mkdir /opt/LOCAL_ASSETSTORE  
sudo chown dsaadmin /opt/LOCAL_ASSETSTORE
~~~

## Create a directory for Mongo
sudo mkdir /opt/MONGO_LOCAL 
sudo chown dsaadmin /opt/MONGO_LOCAL

## maybe put everythin in DSAData  ???

### Default User and password
on initial creation, the userid=admin and password=password
Obviously, this is not very secure.  So we <i>strongly</i> recommend you change
this as follows

However, when you do this, you must also specify the user ID and password when
you do any upgrades to the main docker image.

![](assets\DSA_Installation-694b1617.png)assets/DSA_Installation-694b1.png

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

Viewing Label Images  **WARNING**
Experimental-- view macro images

connect to the docker container

cd plugins
cd large_image
git branch -a
git checkout show-label-images

Should be embedded to make this work in the tag
{"images": ["macro", "label"]}

assets/DSA_Installation-c8460.png


assets/DSA_Installation-c8460.png
