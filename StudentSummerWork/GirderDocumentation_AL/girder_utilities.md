GIRDER DOCUMENTATION
--------------------------------------------------------------
Tasks include how to download an image, how to sync a local image collection with the "GIRDER" version...
how to download a directory, how to list ITEMS in a directory... how to list FILES in an item..
Explain what an item IS!!! I..e. an item can contain many files(that often have the same / similar content)

Code to initialize Girder:

```
import girder_client
API_URL = "http://digitalslidearchive.emory.edu:8080/api/v1"
gc = girder_client.GirderClient(apiUrl=API_URL)
gc.authenticate(interactive=True)
```

Logs you into Girder - prompts for login and password:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-25%20at%203.48.45%20PM.png)
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-25%20at%203.48.55%20PM.png)

To check that you've been logged in, there is no confirmation if correct:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-25%20at%203.49.02%20PM.png)

Only Error if incorrect:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-25%20at%203.49.12%20PM.png)

--------------------------------------------------------------
```
import sys
def recurseGetItems(client, folderID, parentType='folder'):
    folders = []
    folders.extend(client.listFolder(folderID, parentFolderType=parentType))
    items = []

    try:
        items.extend(client.listItme(folderID))
    except:
        items = []
    if len(folders) is not 0:
        for fld in folders:
            items.extend (recurseGetItems(client,fld['id']))
    return items
```

Result: does nothing, copy and pasted in Jupyter Notebooks but no output whatsoever

![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-25%20at%203.15.52%20PM.png)

--------------------------------------------------------------
```
class LinePrinter():
    """
    Print things to stdout on one line dynamically
    """
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()
```

Result: it's a function that'll be used throughout the code. So it does nothing on its own
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-25%20at%203.54.12%20PM.png)


--------------------------------------------------------------
```
rajsFldId = '5b046b8192ca9a001abb1c66'
gbmFldId = '59f7697092ca9a001734c565'

sldList = list(gc.getResource('resource/' + gbmFldId + '/items?type=folder&limit=10000&sort=_id&sortdir=1'))
length = len(sldList)
count = 0

for sld in sldList:
    if '(1)' in sld['name']:
          print sld['name']
          itemData = gc.get('/item?folderId=%s&name=%s&limit=50&offset=0&sort=lowerName&sortdir=1' % (rajsFldId, sld['name']))
          itemData
          break
          if itemData == []:
        gc.post("item/" + sld['_id'] + '/copy', {"folderId": rajsFldId})
          count += 1
      break
      LinePrinter("Slide %s of %s copied." % (count, length))
```

Copies all slides in main and all its subfolders, source:gbmFldID, dest:rajsFldId
works as intended - output reflects its copying and pasting. (1) at the end of the file
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.22.57%20AM.png)

--------------------------------------------------------------
```
rajsFldId = '5ae351e792ca9a0020d95e50'
count =0
for sld in gc.getResource('resource/' + rajsFldId + '/items?type=folder&limit=10000&sort=_id&sortdir=1'):
    if '(' in sld['name']:
        count+=1
print count
```

Counts the slide duplicates, works as intended, but output simply indicates how many copies there are.
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.28.00%20AM.png)

--------------------------------------------------------------
```
rajsFldId = '5ae351e792ca9a0020d95e50'

count =0
for sld in gc.getResource('resource/' + rajsFldId + '/items?type=folder&limit=10000&sort=_id&sortdir=1'):
    if '(' in sld['name']:
        gc.delete("item/" + sld['_id'])
        count+=1

print count
```
delete the duplicated slides, but only indicates number of slides deleted.
works as intended

![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.29.31%20AM.png)

--------------------------------------------------------------
```
rajsFldId = '5ae351e792ca9a0020d95e50'
count =0

for sld in gc.getResource('resource/' + rajsFldId + '/items?type=folder&limit=10000&sort=_id&sortdir=1'):
    count+=1

print count
```

count total number of slides in the folder, works as intended

![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.31.00%20AM.png)
-------------------------------------------------------------------

Getting the sample count for each of the classes¶
Coded by JCV
Last updated: 5/1/2018
Several artifacts in each slide have been labeled as either yes or no to indicate whether the artifact is present or not in the slide. Each class is a permuation of these label (e.g. class 1 is Artifact1=Yes & Artifact2=Yes, class 2 is Artifact1=Yes & Artifact2=No)

dependencies
```
import girder_client
import numpy as np
import pandas as pd
from IPython.display import display, HTML
import itertools

API_URL = "http://digitalslidearchive.emory.edu:8080/api/v1"
gc = girder_client.GirderClient(apiUrl=API_URL)
gc.authenticate(interactive=True)

sourceFldId = '5ae351e792ca9a0020d95e50'
```

 Errors Encountered:
 No. of slides--- unnamed tag 'meta', was unable to retrieve count
 sourceFldId = '5ae351e792ca9a0020d95e5'
 sourceFldId = '5a1b392492ca9a001824c10c'
 KeyError                                  Traceback (most recent call last)
 <ipython-input-22-bdda789adf8f> in <module>()
       3 tags = ['AirBubble', 'Blood', 'Ink']
       4 for sld in gc.listItem(sourceFldId):
 ----> 5     tags_current = sld['meta']['tags']
 6     if all (tag in tags_current for tag in tags):
       7         slidesTagged.append(sld)
 KeyError: 'meta'


```
slidesTagged = []
tags = ['AirBubble', 'Blood', 'Ink']
for sld in gc.listItem(sourceFldId):
    tags_current = sld['meta']['tags']
    if all (tag in tags_current for tag in tags):
        slidesTagged.append(sld)
print 'There are %s labeled slides.' % len(slidesTagged)
```

get set of slides that have the tags of interest
works as intended

![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.33.40%20AM.png)



```
ftLabel = ['Yes','No']
classes = [list(y for y in x) for x in itertools.product(ftLabel, ftLabel, ftLabel)]
counts = [0]*len(classes)
for sld in slidesTagged:
    tc = sld['meta']['tags']
    for i in range(len(counts)):
        if all (tc[tags[j]]==classes[i][j] for j in range(len(tags))):
            counts[i] += 1
            continue
```

get the count for all the possible classes (permuation of tag values). No output, used for the next block of code.

![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.34.44%20AM.png)

```
data = np.hstack((np.array([range(len(classes))]).T, np.array(classes), np.array([counts]).T))
titles = np.hstack((np.array(['Class  ']), np.array(tags), np.array(['Count'])))
df = pd.DataFrame(data)
df = pd.DataFrame(data, columns=titles)
display(HTML(df.to_html(index=False)))
```
use pandas to display the results of number of slides for each class, works as intended

![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.34.50%20AM.png)
--------------------------------------------------------------------------------


Download the images from the Girder

```
import girder_client
API_URL = "http://digitalslidearchive.emory.edu:8080/api/v1"

gc = girder_client.GirderClient(apiUrl=API_URL)
gc.authenticate(interactive=True)
from pprint import pprint
import sys, os
from IPython.display import Image
import urllib

dsaGC = gc.GirderClient(apiUrl="http://adrc.digitalslidearchive.emory.edu:8080/api/v1")

class LinePrinter():
    """
    Print things to stdout on one line dynamically
    """
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

def saveSVSslide(slide, path):
    url =  "http://adrc.digitalslidearchive.emory.edu:8080/api/v1/item/%s/download?contentDisposition=attachment" \
        % slide['_id']
    urllib.urlretrieve(url, path+slide['name'])

folderID = '5ae351e792ca9a0020d95e50'
numImages = len(list(gc.listItem(folderID)))
count = 0

for slide in gc.listItem(folderID):
    count += 1
      pprint(slide)
      break
    LinePrinter("Saving image %s of %s" % (count, numImages))
    path = "/media/raj/Raj1_5/wsi_directory/"
    t = saveSVSslide(slide, path)
```

Output:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.40.02%20AM.png)
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.40.10%20AM.png)

---------------------------------------------
labeled images download

```
import girder_client
API_URL = "http://digitalslidearchive.emory.edu:8080/api/v1"
gc = girder_client.GirderClient(apiUrl=API_URL)
gc.authenticate(interactive=True)
```

```
from pprint import pprint
sourceFldID = '5ae351e792ca9a0020d95e50'
slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('LabelFlag') and \
        sld['meta']['tags']['LabelFlag']:
        slides_lbd.append(sld)
```

get all the slides that have the label flag, aka they have been marked up with ground truth. No output for this one, used for next blocks of code
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.40.54%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
air_yes_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('AirBubble') and \
        sld['meta']['tags']['AirBubble'] == "Yes":
        air_yes_slides_lbd.append(sld)

len(air_yes_slides_lbd)
```

count all the slides that have the AirBubble set to Yes, aka slides have AirBubble, working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.40.59%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
air_no_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('AirBubble') and \
        sld['meta']['tags']['AirBubble'] == "No":
        air_no_slides_lbd.append(sld)

len(air_no_slides_lbd)
```

count all the slides that have the AirBubble set to No, aka slides have no AirBubble, working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.44.39%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
bld_yes_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('Blood') and \
        sld['meta']['tags']['Blood'] == "Yes":
        bld_yes_slides_lbd.append(sld)

len(bld_yes_slides_lbd)
```

count all the slides that have the Blood set to Yes, aka slides have blood. Working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.45.04%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
bld_no_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('Blood') and \
        sld['meta']['tags']['Blood'] == "No":
        bld_no_slides_lbd.append(sld)

len(bld_no_slides_lbd)
```

count all the slides that have the Blood set to No, aka slides have no Blood. working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.45.28%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
ink_yes_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('Ink') and \
        sld['meta']['tags']['Ink'] == "Yes":
        ink_yes_slides_lbd.append(sld)

len(ink_yes_slides_lbd)
```

get all the slides that have the Ink set to Yes, aka slides have Ink. working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.45.44%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
ink_no_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('Ink') and \
        sld['meta']['tags']['Ink'] == "No":
        ink_no_slides_lbd.append(sld)

len(ink_no_slides_lbd)
```

get all the slides that have the Ink set to No, aka slides have no Ink  
working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.49.14%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
sha_yes_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('Sharpie') and \
        sld['meta']['tags']['Sharpie'] == "Yes":
        sha_yes_slides_lbd.append(sld)

len(sha_yes_slides_lbd)
```

get all the slides that have the Sharpie set to Yes, aka slides have Sharpie
if there are no slides marked as Sharpie 0 - working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.47.36%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
sha_no_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('Sharpie') and \
        sld['meta']['tags']['Sharpie'] == "No":
        sha_no_slides_lbd.append(sld)

len(sha_no_slides_lbd)
```

get all the slides that have the Sharpie set to No, aka slides have no Sharpie
0- working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.48.22%20AM.png)


```
print("  of Sharpie   - Yes Slides: "+ str(len(sha_yes_slides_lbd)))
print("  of Sharpie   - No  Slides: "+ str(len(sha_no_slides_lbd)))
print("  of AirBubble - Yes Slides: "+ str(len(air_yes_slides_lbd)))
print("  of AirBubble - No  Slides: "+ str(len(air_no_slides_lbd)))
print("  of Blood     - Yes Slides: "+ str(len(bld_yes_slides_lbd)))
print("  of Blood     - No  Slides: "+ str(len(bld_no_slides_lbd)))
print("  of Ink       - Yes Slides: "+ str(len(ink_yes_slides_lbd)))
print("  of Ink       - No  Slides: "+ str(len(ink_no_slides_lbd)))
print("Total- No  Slides: "+ str(len(slides_lbd)))
```

prints every count we've seen thus far in our code.
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.49.43%20AM.png)

```
sourceFldID = '5ae351e792ca9a0020d95e50'
airbld_yes_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('AirBubble') and \
        sld['meta']['tags']['AirBubble'] == "Yes" and sld['meta']['tags']['Blood'] == "Yes":
        airbld_yes_slides_lbd.append(sld)

        for sld in airbld_yes_slides_lbd:
             print (sld['_id'])

len(airbld_yes_slides_lbd)
```

get all the slides that have the AirBubble and  Blood set to Yes, aka slides have AirBubble and Blood
works - prints out all the slides names and then the number of them.
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.54.50%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
airink_yes_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('AirBubble') and \
        sld['meta']['tags']['AirBubble'] == "Yes" and sld['meta']['tags']['Ink'] == "Yes":
        airink_yes_slides_lbd.append(sld)

len(airink_yes_slides_lbd)
```

get all the slides that have the AirBubble and  Ink set to Yes , aka slides have AirBubble and Ink
working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.55.56%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
bldink_yes_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('Blood') and \
        sld['meta']['tags']['Blood'] == "Yes" and sld['meta']['tags']['Ink'] == "Yes":
        bldink_yes_slides_lbd.append(sld)

len(bldink_yes_slides_lbd)
```

get all the slides that have the Blood and  Ink set to Yes , aka slides have Blood and Ink
working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.57.14%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
all_yes_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('AirBubble') and \
        sld['meta']['tags']['AirBubble'] == "Yes" and \
        sld['meta']['tags']['Blood'] == "Yes" and sld['meta']['tags']['Ink'] == "Yes":
        all_yes_slides_lbd.append(sld)

len(all_yes_slides_lbd)
```

get all the slides that all three markings
working
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.57.31%20AM.png)


```
sourceFldID = '5ae351e792ca9a0020d95e50'
all_no_slides_lbd = []
for sld in gc.listItem(sourceFldID):
    if sld.has_key('meta') and \
        sld['meta'].has_key('tags') and \
        sld['meta']['tags'].has_key('AirBubble') and \
        sld['meta']['tags']['AirBubble'] == "No" and \
        sld['meta']['tags']['Blood'] == "No" and sld['meta']['tags']['Ink'] == "No":
        all_no_slides_lbd.append(sld)

len(all_no_slides_lbd)
```

get all the slides that have none of the three markings
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2011.57.52%20AM.png)

-------------------------------------------------------------
girder_utils - Girder Utilities

```
import girder_client
import HttpError


def recurseGetItems(client, folderId):
    items = list(recurseGetResource(client, folderId, 'item'))
    folders = recurseGetResource(client, folderId, 'folder')

    for folder in folders:
        tmp = recurseGetItems(client, folder["_id"])
        items += list(tmp)

    return items
```

No output
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.23.29%20PM.png)

```
def recurseGetResource(client, parentId, resourceType, parentType='folder'):


        #The recursion logic is broken here...
    """
    Recurse below the parent(indicated by parentId) and generate a list of all
    resources of type resourceType that existed under the parent.

    :param parentId: Id of the collection or folder to be searched.
    :type parentId: ObjectId
    :param resourceType: Either 'item' or 'folder'. Indicates whether nested
    folder data or item data should be collected.
    :type resourceType: str
    :param parentType: Either 'folder' or 'collection'. Indicates whether
    the parentId is a collection id or a folder id.
    :type parentType: str
    :returns: A list of all folders or items below parentId.
    :rtype: list of dict
    """
      #now get all folders
    resourceList = []

    try:
        folders = client.listFolder(parentId, parentFolderType=parentType)
    except girder_client.HttpError as err:
        print err
        print HttpError(err)
        return []

     #The line below is commented and moved below because this is an iterator and
     #it consume the list only once, you will ending extending resourceList to None
    folderIdList = getField(folders, '_id')

    if resourceType is 'item' and parentType is not 'collection':
        try:
            data = client.listItem(parentId)
            resourceList.extend(data)
        except girder_client.HttpError as err:
            print "HTTP Error thrown"

            print HttpError(err)
            print err
            return []
    elif resourceType is 'folder':
        resourceList.extend(folders)
    elif resourceType is not 'item' or resourceType is not 'folder':
        raise Exception('Invalid resourceType: %s' % resourceType)

     #folderIdList is an iterator and can only be consumed once. Do not move it up in the function
    folderIdList = getField(folders, '_id')

        #The recursion does NOT work if you start with a collection.. probably iwll work if it's a folder.
    for folderId in folderIdList:
        resourceList.extend(recurseGetResource(client, folderId, resourceType))

    return resourceList
```

No Output
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.23.39%20PM.png)
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.23.48%20PM.png)


```
def getField(data, strKey):
    return [i[strKey] for i in data]
```

No Output
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.24.30%20PM.png)

```
def getFolderID_for_FolderName_in_ParentFolder( girderClient, folderName, parentFolderID, parentType='folder'):
    """Since a folder name may (or may not) be unique across a collection, or across girder
    This will search for folder FOO in the folder BAR, and will create a folder if it doesn't exist yet"""
    gc = girderClient

    try:
        folderData = gc.createFolder(parentFolderID , folderName, parentType=parentType)
    except:
        requestUrl = 'folder?parentType=%s&parentId=%s&name=%s&limit=50&sort=lowerName&sortdir=1' % (parentType, parentFolderID, folderName)
        folderData = gc.getResource(requestUrl)[0]

    return folderData['_id']
```

No Output
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.24.55%20PM.png)

```
def lookupItemByName(girderClient, parentFolderID, itemName):
    """Sees if an item of FOO already exists in folder BAR"""
    gc = girderClient
    try:
        itemData = gc.get('/item?folderId=%s&name=%s&limit=50&offset=0&sort=lowerName&sortdir=1' % (parentFolderID,itemName ))
        return itemData
        print itemData
    except:
         print "Found no item data"
            #no item found
    return False
```

No output
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.25.24%20PM.png)


```
def copySlideToCuratedFolder( girderClient, itemData, metaData, namingScheme, curatedFolderID ):
    """Assuming namingScheme = ADRC, which creates a subject folder and a stain folder"""

    gc= girderClient

       #Refactor this to maybe just have it uses those keys in a list or something?
    if  namingScheme == 'patientID_stainType':
           #This could maybe recurse based on splitting the namingScheme, but may become hard to read
        firstBranchName = metaData['patientID']
        secondBranchName = metaData['stainType']
        firstBranch_FolderID = getFolderID_for_FolderName_in_ParentFolder( gc,firstBranchName,curatedFolderID)
           # The parent folder for the second branch is what's returned from the previous staement
        secondBranch_FolderID = getFolderID_for_FolderName_in_ParentFolder( gc,secondBranchName,firstBranch_FolderID)

           # Check if item already exists in the targetFolder
        if not lookupItemByName( gc, secondBranch_FolderID, itemData['name']):
            print "Moving the folder to %s / %s " %  ( metaData['patientID'], metaData['stainType'] )
            try:
                gc.post("item/" + itemData['_id'] + '/copy', {"folderId": secondBranch_FolderID})
            except:
                print "failed " + folderName
                pass
```

No Output
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.25.51%20PM.png)

```
def getFolderID_for_FolderName_in_ParentFolder( girderClient, folderName, parentFolderID, parentType='folder'):
    """Since a folder name may (or may not) be unique across a collection, or across girder
    This will search for folder FOO in the folder BAR, and will create a folder if it doesn't exist yet"""
    gc = girderClient

    try:
        folderData = gc.createFolder(parentFolderID , folderName, parentType=parentType)
    except:
        requestUrl = 'folder?parentType=%s&parentId=%s&name=%s&limit=50&sort=lowerName&sortdir=1' % (parentType, parentFolderID, folderName)
        folderData = gc.getResource(requestUrl)[0]

    return folderData['_id']
```

No Output
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.26.30%20PM.png)
---------------------------------------------------------------------------------------------

To create Virtual Folder Structure

```
import girder_client
from girder_utils import recurseGetResource
import json
import pprint
API_URL = "http://adrc.digitalslidearchive.emory.edu:8080/api/v1"

gc = girder_client.GirderClient(apiUrl=API_URL)
gc.authenticate(interactive=True)

topfolder='5ae351e792ca9a0020d95e50'
print gc.listItem(topfolder)

gc.post("item/" + '5ae351e892ca9a0020d95e55' + '/copy', {"folderId": '5ae9da5492ca9a001ae5f908'})

sourceFldID = '5ae9da5492ca9a001ae5f908'
destFldID='5ae9da5492ca9a001ae5f907'
for slide in gc.listItem(sourceFldID):
   gc.post("item/" + slide['_id'] + '/copy', {"folderId": destFldID})


from pprint import pprint
  "LabelFlag": true
for i in gc.listItem(topfolder):
    pprint(i)
    break
```

Output:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.29.43%20PM.png)
-----------------------------------------

create Virtual Folder Structure...

```  
import girder_client
from girder_utils import recurseGetResource
import json
import pprint
API_URL = "http://adrc.digitalslidearchive.emory.edu:8080/api/v1"

gc = girder_client.GirderClient(apiUrl=API_URL)
gc.authenticate(interactive=True)

 # Let's get the project by Name
CollectionName = 'ADRC'
ADRCCollUID =  gc.resourceLookup('/collection/%s' % CollectionName)

 #  Let's also get the projectMetadata folder for this collection
metaDataFolder =  list(gc.listFolder(ADRCCollUID['_id'],parentFolderType='collection',name='.projectMetaData'))[0]
pprint.pprint(metaDataFolder)

  #   For the first iteration, I want to bootstrap this with the list of patient folders we have already created
patientFolder = gc.listFolder('5a2039e592ca9a0018254053')

patientIDList = [x['name'] for x in patientFolder]
print patientIDList

  #  Be Careful you don't overwrite the projectScheme with whatever you manually edit here... unless you mean to do it

stainType = ["TDP","TAU","AB","SYN","UBIQ","BIEL","HE","SM","THIO","LFB","NF"]
patientID = [u'A01-94', u'A03-138', u'A11-120', u'A12-62', u'A16-15', u'A16-24', u'A16-27', u'A16-33', u'A16-34', u'E04-125', u'E04-155', u'E04-48', u'E04-76', u'E04-99', u'E05-100', u'E05-108', u'E05-194', u'E05-200', u'E06-06', u'E06-112', u'E06-160', u'E06-18', u'E06-52', u'E06-97', u'E07-48', u'E07-85', u'E08-119', u'E08-146', u'E08-162', u'E09-08', u'E09-155', u'E09-164', u'E09-35', u'E09-81', u'E09-91', u'E10-110', u'E10-129', u'E10-137', u'E10-150', u'E10-151', u'E10-160', u'E10-179', u'E10-38', u'E10-48', u'E10-56', u'E10-63', u'E10-81', u'E10-83', u'E10-88', u'E11-112', u'E11-124', u'E11-125', u'E11-128', u'E11-139', u'E11-143', u'E11-20', u'E11-41', u'E11-59', u'E11-60', u'E11-70', u'E11-71', u'E11-73', u'E11-75', u'E11-81', u'E11-83', u'E11-84', u'E11-97', u'E12-06', u'E12-110', u'E12-120', u'E12-14', u'E12-32', u'E12-64', u'E12-74', u'E12-85', u'E15-01', u'E15-101', u'E15-106', u'E15-110', u'E15-111', u'E15-125', u'E15-132', u'E15-140', u'E15-30', u'E15-45', u'E15-46', u'E15-92', u'E15-97', u'E16-11', u'E16-110', u'E16-114', u'E16-123', u'E16-128', u'E16-131', u'E16-138', u'E16-16', u'E16-18', u'E16-19', u'E16-21', u'E16-45', u'E16-66', u'E17-05', u'E17-12', u'E17-17', u'E17-21', u'E17-22', u'E17-32', u'E17-36', u'E17-39', u'E17-40', u'E17-47', u'OS00-10', u'OS00-11', u'OS00-14', u'OS00-19', u'OS00-21', u'OS00-40', u'OS00-41', u'OS01-02', u'OS01-06', u'OS01-10', u'OS01-134', u'OS01-152', u'OS01-33', u'OS01-60', u'OS03-300', u'OS03-385', u'OS03-95', u'OS160608', u'OS161018', u'OS86-04', u'OS89-44', u'OS93-24', u'OS96-33', u'OS97-60', u'OS97-61', u'OS99-04', u'OS99-07', u'OS_170124']

projectSchema = { 'stainType': stainType, 'patientID': patientID}
print projectSchema

  #  Be careful... updating the projectSchema here..
gc.addMetadataToFolder(metaDataFolder['_id'],{ 'projectSchema': projectSchema} )
  # We may also want to keep other things here like TotalSlides, TotalPatients, TotalStains, whatever as top level parameters

  # Going to now go through the projectSchema and create a virtual folder structure, in this first example
  # I am creating a folder structure based on patientID-->stainType
  # We may also do patientID-->Region-->StainType or other iterations in other examples below
  # Let's get the project by Name
CollectionName = 'ADRC.VirtualFolderStructure'
virtualADRCCollUID =  gc.resourceLookup('/collection/%s' % CollectionName)

  # First create it by Patient and then by Stain
TopLevelFolderName = "ByPatient"
TLF = gc.createFolder(virtualADRCCollUID['_id'],TopLevelFolderName,parentType='collection',reuseExisting=True)


  # We now create a folder for every patient, and then a separate folder by stain
for pt in projectSchema['patientID']:
    #   Now create a virtual folder for each patient...
    virtualPatientFolder  = gc.createFolder(TLF['_id'],pt,description=pt,reuseExisting=True)

    for stain in projectSchema['stainType']:
        params = { "parentType": "folder",
               "parentId"  : virtualPatientFolder['_id'],
               "reuseExisting": True,
               "description" : stain,
               "name":         stain,
                "isVirtual": True,
                "virtualItemsQuery": json.dumps({"meta.stainType": stain,  "meta.patientID": pt, 'baseParentId': {"$oid": ADRCCollUID['_id']}})
                 }
        virtualStainFolder =  gc.post("folder",parameters=params)
     #  CREATE AN ALL FOLDER FOR EVERYTHING
    params = { "parentType": "folder",
           "parentId"  : virtualPatientFolder['_id'],
           "reuseExisting": True,
           "description" : 'ALL',
           "name":         'ALL',
            "isVirtual": True,
           "virtualItemsQuery": json.dumps({ "meta.patientID": pt})
             }
    anyPtSlide =  gc.post("folder",parameters=params)
  # As a cleanup step, I need to delete virtualFolders that contain 0 virtualItems, as it's annoying
  # alhttp://localhost:8890/notebooks/createADRCVirtualFolderStructure.ipynb though we could also change the UI to not render them ... TBD


print TLF['_id']
print list(gc.listFolder(TLF['_id']))
   #  Let's look for empty folders...
virtualPtFolderList =  list( gc.listFolder(TLF['_id'],parentFolderType='folder') )

ptsProcessed = 0

for vpf in virtualPtFolderList:
     #   Let's now see what's in each of these folders
    ptsProcessed += 1

    ptByStainFolders = gc.listFolder(vpf['_id'])
    for pbsf in ptByStainFolders:
        itemsInCurFolder =  list(gc.listItem(pbsf['_id']))
        print len(itemsInCurFolder),pbsf['name'],vpf['name']
        if len(itemsInCurFolder) == 0:
             gc.delete('/folder/%s'%pbsf['_id'])
             print "Deleting %s for pt %s which has %d items" % ( pbsf['name'],vpf['name'], len(itemsInCurFolder))


    #  Delete the TopLevel Folder if it has no virtual folders in it..

  # First create it by Patient and then by Stain
  #   Let's look for empty folders...
virtualPtFolderList =  list( gc.listFolder(TLF['_id'],parentFolderType='folder') )

print virtualPtFolderList

  for vpf in virtualPtFolderList:
      print vpf['name']

   #  We now create a folder for every patient, and then a separate folder by stain
  for pt in projectSchema['patientID']:
    #     Now create a virtual folder for each patient...
      virtualPatientFolder  = gc.createFolder(TLF['_id'],pt,description=pt,reuseExisting=True)


  # Organize by Region MetaData Key
  # Folder Name is VF.ByRegion
ByRegionFolderID = '5a94567b92ca9a00186a2f4d'


 folder?parentType=folder&parentId=5a94567b92ca9a00186a2f4d&name=Cerebellum&description=Cerebellum%20slides&reuseExisting=true&isVirtual=true&virtualItemsQuery=%7B%22meta.brainRegion%22%3A%22Cerebellum%22%7D
regionList = ["Amygdala","BasalGanglia","BasalGanglia_NucleusBasalis","Cerebellum","CingulateCortex","FrontalCortex",
"Hippocampus","InsularCortex","Medulla","OccipitalCortex","ParietalCortex","PeriRolandic_eight","PeriRolandic_seven","Pons","TemporalCortex"]

for regionName in regionList:

    folderGenQuery=  "{\"meta.brainRegion\":\"%s\"}" % regionName
    postRoute = "folder?parentType=folder&parentId=%s&name=%s&description=%s&reuseExisting=true&isVirtual=true&virtualItemsQuery=%s"
    postRoute_wp = postRoute % ( ByRegionFolderID, regionName, regionName, folderGenQuery)
    print regionName
    gc.post(postRoute_wp)
```

Output:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.36.08%20PM.png)
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.36.19%20PM.png)
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.36.29%20PM.png)
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.36.37%20PM.png)

--------------------------------------------------

These next few all have invalid syntax as their error.
```
case 'getCollURL':
      url = config.BASE_URL + "/resource/lookup?path=collection/" + config.COLLECTION_NAME;
      promise = makePromise(url);
      break;
```
Output:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.37.01%20PM.png)

```
case 'listFoldersInCollection':
      url = config.BASE_URL + "/folder?limit=1000&parentType=collection&parentId=" + girderObjectID;
      promise = makePromise(url);
      break;
```

Output:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.37.10%20PM.png)

```
case 'listFoldersinFolder':
      url = config.BASE_URL + "/folder?parentType=folder&parentId=" + girderObjectID;
      promise = makePromise(url);
      break;
                //adrc.digitalslidearchive.emory.edu:8080/api/v1/item?folderId=5ad11d6a92ca9a001adee5b3&limit=50&sort=lowerName&sortdir=1
```

Output:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.37.29%20PM.png)

```
case 'listItemsInFolder':
      url = config.BASE_URL + "/item?folderId=" + girderObjectID + "&limit=5000"
      // url = config.BASE_URL + "/item?limit=500&folderId=" + girderObjectID;
      promise = makePromise(url);
      break;
```

Output:
![alt text](https://github.com/al97/Girder-Documentation/blob/master/Screen%20Shot%202018-07-30%20at%2012.37.43%20PM.png)

------------------------------------------

Added on 07/16/2018

```
def get_collection_id(gc, collection_name):
      given a girder client object that is authenticated and a collection name,
      returns the id of the collection.
    try:
        return gc.get("resource/lookup?path=collection/%s" % collection_name)['_id']
    except:
        raise ValueError("There is no collection with that name.")
```

```
def listResources(gc, endpoint_id, endpoint_type='collection', limit=50000):
      given collection/folder name or id, it returns a list of items
      under the endpoint recursively.
    try:
        return list(gc.listResource("resource/%s/items?type=%s" % (endpoint_id, endpoint_type), limit=limit))
    except:
        raise ValueError("The id does not match any endpoint id in the DSA.")
```

```
def correct_stain(stain, stainTypes = ['Biels','HE','LFB_PAS','Tau','Ubiq', \
                      'aBeta','aSyn','pTDP', 'NF', 'SM', 'Thio']):
      given a list of stain types, this functions tries to re-spell the stains metadata tag
      in the appropriate spelling (don't want multiple spellings for same stain type).
      If after regex resubstitution the stain is not in the list, it returns unknown stain.
    stain = re.sub('(?i)(ab)','aBeta',stain)
    stain = re.sub('(?i)(at8|tau)','Tau',stain)
    stain = re.sub('(?i)(he|h&e)','HE',stain)
    stain = re.sub('(?i)(biel)','Biels',stain)
    stain = re.sub('(?i)(lfb)','LFB_PAS',stain)
    stain = re.sub('(?i)(nf)','NF',stain)
    stain = re.sub('(?i)(ptpd|tdp)','pTDP',stain)
    stain = re.sub('(?i)(s-m|sm)','SM',stain)
    stain = re.sub('(?i)(syn)','aSyn',stain)
    stain = re.sub('(?i)(ubiq)','Ubiq',stain)
    stain = re.sub('(?i)(thiof|thoif)','Thio',stain)
    stain = re.sub('(?i)(thio|thoi)','Thio',stain)
    if stain in stainTypes:
        return stain
    else:
        return 'unknown'
```

```
def clean_metadata(metadata):
      cleans the metadata to remove unwanted leading and trailing chracters.
      Cleans the stain type and block ID.
    clean_metadata = {}
    for k, v in metadata.iteritems():
        if k == 'stainType':
            clean_metadata[k] = correct_stain(v.strip('_|-| '))
        else:
            if k == 'blockID':
                v = 'unknown' if v == '' else v.upper()
            clean_metadata[k] = v.strip('_|-| ')
    return clean_metadata
```

```
class LinePrinter():
    """
    Print things to stdout on one line dynamically.
    """
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()
```



--------------
copy all slides in a folder to another folder :
must define itemID separately

for slide in gc.listItem(sourceFldID):
 gc.post("item/" + slide['_id'] + '/copy', {"folderId": destFldID})

 ![alt text](get_2 -- send to Albert)
-----------------------------------------------------------------
def recurseGetItems(client, folderID, parentType='folder'):
    '''
    Returns a list of json objects representing the items inside the folderID given in the appropriate api
    This algorithm implements recursion method

    INPUTS
    client - a girder client object
    folderId - a string id of the folder or collection
    parentType - only needs to be modified if your folderId is for a collection (see above)

    OUTPUT
    items - an array containing slide info
    '''
    folders = []
    folders.extend(client.listFolder(folderID, parentFolderType=parentType))
    items = []
    try:
        items.extend(client.listItem(folderID))
    except:
        items = []

    if len(folders) is not 0:
        for fld in folders:
            items.extend(recurseGetItems(client, fld['_id']))
    return items


def lookupItemByName( girderClient, parentFolderID, itemName):
    """Sees if an item of FOO already exists in folder BAR"""
    gc = girderClient
    try:
        itemData = gc.get('/item?folderId=%s&name=%s&limit=50&offset=0&sort=lowerName&sortdir=1' % (parentFolderID,itemName ))
        return itemData
    except:
            no item found
        return False


def getFolderID_for_FolderName_in_ParentFolder( girderClient, folderName, parentFolderID, parentType='folder'):
    """Since a folder name may (or may not) be unique across a collection, or across girder
    This will search for folder FOO in the folder BAR, and will create a folder if it doesn't exist yet"""
    gc = girderClient

    try:
        folderData = gc.createFolder(parentFolderID , folderName, parentType=parentType)
    except:
        requestUrl = 'folder?parentType=%s&parentId=%s&name=%s&limit=50&sort=lowerName&sortdir=1' % (parentType, parentFolderID, folderName)
        folderData = gc.getResource(requestUrl)[0]

    return folderData['_id']


def copySlideToCuratedFolder( girderClient, itemData, metaData, curatedFolderID, patientID):
    '''
    Two level copying a slide to a folder. This is tailored to work with a patient ID top level and a stain type nested folder
    level. It also puts slides in an unknown subfolder if a condition is met (see below)

    INPUTS
    giderClient: initiated to the right api
    itemData: the girder client dictionary containign the name and _id of slide (plus metadata is available)
    metaData: contains the metadata or None if the slide should go in the unknown folder
    curatedFolderID: id of the destination folder
    patientID: id of the patient, TOP level folder identifier (e.g. ADRCXX-XX)
    '''
     if the slide was bad, metaData was passed as None
    gc= girderClient

       Refactor this to maybe just have it uses those keys in a list or something?
    if metaData is None:
         Here is the logic for when you want to put the slide into the uknown folder. I need to check if the folder
         for this patient exists. It doesn't I should create a subfolder named unknown (similar to how the stain type and
         patient folder are made
        firstBranchName = patientID
        secondBranchName = 'unknown'
    else:
           This could maybe recurse based on splitting the namingScheme, but may become hard to read
        firstBranchName = patientID
        secondBranchName = metaData['stainType']

    firstBranch_FolderID = getFolderID_for_FolderName_in_ParentFolder( gc,firstBranchName,curatedFolderID)
        The parent folder for the second branch is what's returned from the previous staement
    secondBranch_FolderID = getFolderID_for_FolderName_in_ParentFolder( gc,secondBranchName,firstBranch_FolderID)
        Check if item already exists in the targetFolder
    if not lookupItemByName( gc, secondBranch_FolderID, itemData['name']):
        print "Moving the folder to %s / %s " %  ( patientID, secondBranchName )
        try:
            gc.post("item/" + itemData['_id'] + '/copy', {"folderId": secondBranch_FolderID})
        except:
            pass


def validateSlideMetaData( slideMetaData, validStainTypes ):
    '''
    Checks to see if the stain type of the metadata matches one of the designated stain types. Also checks that the
    metadata contains a patient ID tag. Also it checks that the blockID of the metadata is not too long, which would
    indicate an error

    INPUTS:
    slideMetaData: dictionary containing the metadata
    validStainTypes: an array containing the valid stain types

    OUTPUTS:
    returns an array containing error information of why the slide does not match the pattern (either patientID missing,
        block ID too long, or stain type not valid. It also returns True is slide is good (passed all tests) or False if
        it failed one or more
    '''

    errors = []

    if slideMetaData['stainType'] not in validStainTypes:
        errors.append(('StainType',slideMetaData['stainType']))

    if not slideMetaData['patientID']:
         errors.append(('InvalidPatientID',slideMetaData['patientID']))

    if len(slideMetaData['blockID']) > 4:  correction from DG, previously !=2
         errors.append(('InvalidBlockID',slideMetaData['blockID']))


    if len(errors) > 0:
        return (False, errors)
    else:
        return (True, [])


def create_curated_folder(girderClient, FolderToCurate_ID, TargetFolder_ID, stain_Types, make_unknown=True, ommit=[]):
    """
    A routine that takes in a starting folder in the API and a destination folder, and reorganizes the data
    to match a speficied format. In short, it creates a folder structure that is grouped by desired metadata found in the
    slide files (e.g. group by patient ID followed by grouping by stainType

    INPUTS:
        girderClient: initialized outside the function and must be the desired api (e.g. ADRC)
        FolderToCurate_ID: id of the folder that currently has the slides
        TargetFolder_ID: id of the destination folder (does not have to be empty but must be created beforehand)
        stain_Types: an array of strings corresponding to the stain types that should be recognized
    OPTIONAL_INPUTS:
        make_unknown: default is True and results in slides that don't match the stain type given to be put in their own
            unkown subfolder. If False
        ommit: if you know there is a folder(s) you don't want include, then pass that string name in ommit array
    OUTPUT:
        stats: dictionary with two keys. SlidesThatFailed contains the name of the slides that did not match the format.
            Errors contains info on why the slides specifically failed
    """
    gc = girderClient
    SlidesThatFailed = []
    allerrors = []

    for folder in gc.listFolder(FolderToCurate_ID):  list all folders, one level down from collection
        if folder['name'] not in ommit:
             the folders also have the patient ID, so could get these via regex to deal with the unknown cases
            patientID = folder['name']  from folder name, NOT metadata

            curPatientData = recurseGetItems(gc,folder['_id'])  get all the slides in each folder
            for cpd in curPatientData:  for each slide
                if cpd['name'].endswith(('ndpi','svs')) :  these are the valid slides, so for each slide
                        let's figure out what metadata keys we need in order to be happy about the slide
                    try:
                        (metaDataGood,errors) =  validateSlideMetaData( cpd['meta'] , stain_Types)
                        if len(errors) != 0:
                            allerrors.append(errors)
                    except:
                        print "No metadata for", cpd['name']
                        continue
                    if metaDataGood:  only true if it passed the above
                        copySlideToCuratedFolder(gc, cpd, cpd['meta'], TargetFolder_ID, patientID)
                    else:
                        if make_unknown:
                            copySlideToCuratedFolder(gc, cpd, None, TargetFolder_ID, patientID)
                        SlidesThatFailed.append(cpd['name'])
        else:
            print 'Skipping folder name:',folder['name']
    stats = dict([('SlidesThatFailed',SlidesThatFailed),('Errors', allerrors)])
    return stats

'''
def recurseGetItems(client, folderId, parentType='folder', printLog=False):

    JCV: This function was modified to handle cases when the folder id corresponds to a collection instead of a folder
    In this case it requires an optional parameter (parentType) to be set to collection

    INPUTS
    client - a girder client object
    folderId - a string id of the folder or collection
    parentType - only needs to be modified if your folderId is for a collection (see above)
    printLog - set to True to informative output to be printed (only works for collection Ids)

    OUTPUT
    slideDict - when dealing with collections it returns a dictionary with the slides info in a folder structure
    items - an array containing slide info


    if parentType=='collection':
        topLevelFolders = client.listFolder(folderId, parentFolderType=parentType)
        slideDict = {}  Dict where the top level key is the folder name, and below are the slides in that folder

        for tlf in topLevelFolders:
            slidesInFolder = recurseGetItems(client, tlf['_id'])
            if printLog:
                print "Retrieving slides in",tlf['name'],";", len(slidesInFolder),"files are in the current folder"
            slideDict[tlf['name']] = slidesInFolder
        return slideDict
    else:
        items = list(recurseGetResource(client, folderId, 'item'))
        folders = recurseGetResource(client, folderId, 'folder')

        for folder in folders:
            tmp = recurseGetItems(client, folder["_id"])
            items += list(tmp)

        return items

def recurseGetResource(client, parentId, resourceType, parentType='folder'):


        The recursion logic is broken here...
    """
    Recurse below the parent(indicated by parentId) and generate a list of all
    resources of type resourceType that existed under the parent.
    :param parentId: Id of the collection or folder to be searched.
    :type parentId: ObjectId
    :param resourceType: Either 'item' or 'folder'. Indicates whether nested
    folder data or item data should be collected.
    :type resourceType: str
    :param parentType: Either 'folder' or 'collection'. Indicates whether
    the parentId is a collection id or a folder id.
    :type parentType: str
    :returns: A list of all folders or items below parentId.
    :rtype: list of dict
    """
      now get all folders
    resourceList = []

    try:
        folders = client.listFolder(parentId, parentFolderType=parentType)
    except girder_client.HttpError as err:
        print err
         print HttpError(err)
        return []

     The line below is commented and moved below because this is an iterator and
     it consume the list only once, you will ending extending resourceList to None
     folderIdList = getField(folders, '_id')

    if resourceType is 'item' and parentType is not 'collection':
        try:
            data = client.listItem(parentId)
            resourceList.extend(data)
        except girder_client.HttpError as err:
            print "HTTP Error thrown"

             print HttpError(err)
            print err,
            return []
    elif resourceType is 'folder':
        resourceList.extend(folders)
    elif resourceType is not 'item' or resourceType is not 'folder':
        raise Exception('Invalid resourceType: %s' % resourceType)

     folderIdList is an iterator and can only be consumed once. Do not move it up in the function
    folderIdList = getField(folders, '_id')

        The recursion does NOT work if you start with a collection.. probably iwll work if it's a folder.
    for folderId in folderIdList:
         if re
        resourceList.extend(recurseGetResource(client, folderId, resourceType))

    return resourceList

def getField(data, strKey):
    return [i[strKey] for i in data]
'''
