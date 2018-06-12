I am installing Nvidia Docker (and Docker) on a brand new Ubuntu 16.04 machine


### Following initial info from here
https://websiteforstudents.com/install-proprietary-nvidia-gpu-drivers-on-ubuntu-16-04-17-10-18-04/

    sudo add-apt-repository ppa:graphics-drivers/ppa
    sudo apt-get update
    sudo apt-get install nvidia-387
   
   sudo reboot
   
   
Wait while the machine reboots, then work on adding docker


## If you have already installed docker before, check out here
https://docs.docker.com/install/linux/docker-ce/ubuntu/#prerequisites
   
   
 
    sudo apt-get install \
     apt-transport-https \
      ca-certificates \
     curl \
     software-properties-common
   

 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo -E apt-key add -

then add the repoisotry

    sudo -E add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

##### The -E exports any env variables from my non sudo user, in this case it exports the https_proxy info I describe below

### Dealing with weird proxy issues

Some of my GPU servers are behind a proxy, so I head to type this in first

export https_proxy='https://170.140.138.165:8000/'
export http_proxy='http://170.140.138.165:8000/'

#### Now install docker CE
    sudo apt-get install docker-ce
    
    
#### Actually using docker!

so 'docker ps' should show you a list of running containers; however you can only access docker if you are a member of the docker user group

    sudo usermod -a -G docker dagutman
    
Adds userid dagutman to the docker group; however you still have to log off then relog back in so the new group permissions are actually applied to your session



### WHEN WEIRD STUFF HAPPENS

Curl stopped working for some reason after I rebooted

    sudo apt-get install libcurl4-openssl-dev

Seemed to fix it

