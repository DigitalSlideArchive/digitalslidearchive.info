"""Collection of functions that wrap around multiple girder
client functions for specific goal."""
import girder_client
import numpy as np
from PIL import Image
from io import BytesIO

def test():
    print("This is a test!")

def login(api_url, private=True):
    """login() 
    Connects to chosen girder API.
    
    INPUTS
    ------
    api_url : str
        Url to the API to connect to (i.e. servername/api/v1).
    private : bool
        True to interactively authenticate (to access private items)
        or False if accessing public items.
        
    RETURNS
    -------
    gc : girder_client.GirderClient
        Girder client connected to a girder API.
    """
    gc = girder_client.GirderClient(apiUrl=api_url)
    if private:
        gc.authenticate(interactive=True)
    return gc

def get_collection(gc, name):
    """get_collection() 
    Get the info of a girder collection by its name.
    
    INPUTS
    ------
    gc : girder_client.GirderClient
        Girder client connected to a girder API.
    name : str
        Name of the collection.
        
    RETURNS
    -------
    collection : dict
        Information about the collection.
    """
    collection = gc.resourceLookup("/collection/%s" % name)
    return collection

def get_items(gc, _id, dirType='folder', limit=50):
    """get_recource()
    Get all items, recursively, in a folder or collection. Does not
    work with items in a virtual folder.
    
    INPUTS
    ------
    gc : girder_client.GirderClient
        Girder client connected to a girder API
    _id : str ('folder' or 'collection')
        Girder id of folder/collection to get items from.
    limit : int (default 50)
        Maximum amount of girder items to return. May return less
        if there are not enough items.
        
    RETURNS
    -------
    items : list
        List of girder items in that folder/collection.
    """
    items = gc.getResource("resource/%s/items?type=%s&limit=%s&sort=_id&sortdir=1" % \
                  (_id, dirType, limit))
    return items

def get_label_image(gc, _id, width=256, height=256, array=False):
    """get_label_image()
    Given a girder id, get the label image if it exists otherwise throws error.
    
    INPUTS
    ------
    gc : girder_client.GirderClient
        Girder client connected to a girder API.
    _id : str (item)
        Girder id of item to get label for.
    width : int (default 256)
        Width to return label image.
    height : int (default 256)
        Height to return label image.
    array : bool (default False)
        True to return label image in ndarray form, False to return PIL image.
        
    RETURNS
    -------
    image : PIL image or ndarray
        Label image.
    """
    content = gc.get('item/%s/tiles/images/label?width=%s&height=%s&encoding=JPEG' % \
                   (_id, width, height), jsonResp=False)
    image = Image.open(BytesIO(content.content))
    if array:
        image = np.array(image)
    return image
    
def collection_items(gc, name, limit=50):
    """collection_items()
    Get all items in this collection, recursively.
    
    INPUTS
    ------
    gc : girder_client.GirderClient
        Girder client connected to a girder API.
    name : str
        Collection name.
    limit : int (default 50)
        Maximum number of items to return from collection.
        
    RETURNS
    -------
    items : list
        List containing information about items in the collection.
    """
    _id = get_collection(gc, name)['_id']
    items = get_items(gc, _id, dirType='collection', limit=limit)
    return items