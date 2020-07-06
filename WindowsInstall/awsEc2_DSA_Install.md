## I have set up an EC2 instance using t2.large and Windows Server 2016

The instructions are based on this, but with some additional images.

https://github.com/DigitalSlideArchive/digital_slide_archive/blob/master/ansible/README.rst


![](gitInstallUrl_DSA.png)...


![](gitDL_Pic2.png)

## First snag in AWS

I need to adjust my security settings so I can download the file!

![](Snag1_2020-07-06-12-44-52.png)


## Adding Trusted Sites

![](AddingTrustedSites_2020-07-06-12-46-15.png)

https://www.top-password.com/blog/server-2016-your-current-security-settings-do-not-allow-this-file-to-be-downloaded/

![](2020-07-06-12-47-52.png)



## Click on the gear icon and you can adjust security settingsunder Internet Options

![](2020-07-06-12-48-25.png)


I found this fairly confusing, so I enabled download for the "internet" zone and then just installed Google Chrome!

https://google.com/chrome/


Installing Git, which I downloaded via chrome to make life easier.


![](2020-07-06-12-56-51.png)


## Installing VirtualBox

![](2020-07-06-13-00-07.png)

## Installing Vagrant

![](2020-07-06-13-01-38.png)


## Clone the repo via Git Bash

There are multiple ways to grab the DSA repo, but I'll demonstrate just cloning via the GIT commandline tool



![](2020-07-06-13-10-08.png)

Once you've started the 'Git Bash' terminal, type
   
    git clone https://github.com/DigitalSlideArchive/digital_slide_archive.git

    cd digital_slide_archive

    vagrant up


![](2020-07-06-13-12-08.png)


## Vagrant up command will then download the virtual machines, code, etc..
![](2020-07-06-13-12-32.png)
