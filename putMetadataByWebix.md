This uses webix ajax put requests to update the metadata field for an item 



var metaUrl = config.BASE_URL + "/item/" + slideID;

webix.ajax().put(metaUrl,{"metadata": { "hello":"world"}},function(text,xml,xhr) {
webix.message("Put Request has fired")

} )


