import girder_client
#import HttpError


def recurseGetItems(client, folderId):
    items = list(recurseGetResource(client, folderId, 'item'))
    folders = recurseGetResource(client, folderId, 'folder')
   
    for folder in folders:
        tmp = recurseGetItems(client, folder["_id"])
        items += list(tmp)

    return items

def recurseGetResource(client, parentId, resourceType, parentType='folder'):


    ### The recursion logic is broken here...
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
    # now get all folders
    resourceList = []

    try:
        folders = client.listFolder(parentId, parentFolderType=parentType)
    except girder_client.HttpError as err:
        print err
#        print HttpError(err)
        return []

    #The line below is commented and moved below because this is an iterator and 
    #it consume the list only once, you will ending extending resourceList to None
    #folderIdList = getField(folders, '_id')

    if resourceType is 'item' and parentType is not 'collection':
        try:
            data = client.listItem(parentId)
            resourceList.extend(data)
        except girder_client.HttpError as err:
            print "HTTP Error thrown"

#            print HttpError(err)
            print err
            return []
    elif resourceType is 'folder':
        resourceList.extend(folders)
    elif resourceType is not 'item' or resourceType is not 'folder':
        raise Exception('Invalid resourceType: %s' % resourceType)

    #folderIdList is an iterator and can only be consumed once. Do not move it up in the function
    folderIdList = getField(folders, '_id')

    ### The recursion does NOT work if you start with a collection.. probably iwll work if it's a folder.
    for folderId in folderIdList:
        #if re
        resourceList.extend(recurseGetResource(client, folderId, resourceType))

    return resourceList

def getField(data, strKey):
    return [i[strKey] for i in data]



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

def lookupItemByName( girderClient, parentFolderID, itemName):
    """Sees if an item of FOO already exists in folder BAR"""
    gc = girderClient
    try:
        itemData = gc.get('/item?folderId=%s&name=%s&limit=50&offset=0&sort=lowerName&sortdir=1' % (parentFolderID,itemName ))
        return itemData
        #print itemData
    except:
        #print "Found no item data"
        ### no item found
        return False
def copySlideToCuratedFolder( girderClient, itemData, metaData, namingScheme, curatedFolderID ):
    """Assuming namingScheme = ADRC, which creates a subject folder and a stain folder"""
    
    gc= girderClient
    
    ## Refactor this to maybe just have it uses those keys in a list or something?
    if  namingScheme == 'patientID_stainType':
        ## This could maybe recurse based on splitting the namingScheme, but may become hard to read
        firstBranchName = metaData['patientID']
        secondBranchName = metaData['stainType']
        firstBranch_FolderID = getFolderID_for_FolderName_in_ParentFolder( gc,firstBranchName,curatedFolderID)
        ### The parent folder for the second branch is what's returned from the previous staement
        secondBranch_FolderID = getFolderID_for_FolderName_in_ParentFolder( gc,secondBranchName,firstBranch_FolderID)
        
        ### Check if item already exists in the targetFolder
        if not lookupItemByName( gc, secondBranch_FolderID, itemData['name']):
            print "Moving the folder to %s / %s " %  ( metaData['patientID'], metaData['stainType'] )
            try:
                gc.post("item/" + itemData['_id'] + '/copy', {"folderId": secondBranch_FolderID})
            except:
                print "failed " + folderName
                pass

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
