# digitalslidearchive.info
## What is the Digital Slide Archive?

The Digital Slide Archive (DSA) is an open-source platform for the visualization and management of whole-slide digital pathology image data. This project grew out of a resource that we created called *Cancer Digital Slide Archive* (CDSA) that enables users to interact with digital pathology images from The Cancer Genome Atlas. With funding from the National Cancer Institute (U24CA19436201) we are developing this platform to enable others to manage and share their own digital pathology datasets. This project is being developed in collaboration with Kitware, Inc. to create a platform that is open, extensible, and easy to install. Docker technology is used to simplify deployment and portability of established DSA servers.

## The DSA, Girder and HistomicsTK
This project comprises three related efforts:
1. DSA - a front-end platform that enables users to manage, visualize, and annotate their images, and to manage users and access priviliges.
2. Girder - an underlying frameworks providing APIs for data management, authentication, and analysis job and resource management. 
3. HistomicsTK - a python algorithm library for pathology image analysis.

See the [DSA installation guide](https://github.com/DigitalSlideArchive/digitalslidearchive.info/blob/master/DSA_Girder_Installation/DSA_Installation.md) to get started with setting up your own local DSA instance.
