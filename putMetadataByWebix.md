This uses webix ajax put requests to update the metadata field for an item 



var metaUrl = config.BASE_URL + "/item/" + slideID;

webix.ajax().put(metaUrl,{"metadata": { "hello":"world"}},function(text,xml,xhr) {
webix.message("Put Request has fired")

} )


## Update a folder's name using the same URL
I want to change a folder's name, and also add some metadata using AJAX

var metaUrl = config.BASE_URL + "/folder/" + folderID;

webix.ajax().put(metaUrl+"?name="+newFolderName,{"metadata": { "oldFolderName":"ADRC51-06"}},function(text,xml,xhr) {
webix.message("Put Request has fired")

} )




