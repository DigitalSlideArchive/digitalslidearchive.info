DSA API Documentation
--------------------------------------------------------------
Get: List or search for items.

API Listing:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-25%20at%204.07.09%20PM.png)

Notebook Code and Output:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-25%20at%202.50.58%20PM.png)

Looks like it works as intended.

--------------------------------------------------------------
Put: Edit an item or move it to another folder.

API Listing:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-25%20at%204.18.34%20PM.png)

Notebook Code and Output:

The command I wrote moves an item with ID 5b4ccb0592ca9a001ae72b00 from /rajs/girdertasks/alberttest, to /rajs/girdertasks/alberttest2, and back. For this particular command, I will include what each folder looks like before and after. Later on, just assume that all commands utilize these two particular test folders that you can test out yourself.

First command moving from alberttest to alberttest2
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-25%20at%204.18.50%20PM.png)

Second command moving it back
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-25%20at%204.19.40%20PM.png)

--------------------------------------------------------------
Delete: Self-explanatory. Delete by ID.

API Listing:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%2012.14.33%20PM.png)

Notebook Code and Output:

Made some files to try deletion in the alberttest folder. Try them out. Works as intended.
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%2012.15.14%20PM.png)

--------------------------------------------------------------
Copy: Copies the item and reproduces it in that same folder. If you specify a folderId, it'll paste it to that folder.

API Listing:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%2012.23.01%20PM.png)

Notebook Code and Output:
Making a copy in original folder:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%2012.22.52%20PM.png)

Copy-Pasting to a new folder:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%203.39.27%20PM.png)

Copied some files in the alberttest folder. Works as intended.

--------------------------------------------------------------
Download: Downloads the item that you specify.

API Listing:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%203.50.33%20PM.png)

Notebook Code and Output:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%203.50.04%20PM.png)

Can't get it to download. Works as intended on the API listing itself but the python code stalls out.

--------------------------------------------------------------
Files: Gets the files within the item.

API Listing:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%203.47.30%20PM.png)

Notebook Code and Output:
![alt text](https://github.com/al97/DSA_API_Documentation/blob/master/Screen%20Shots/Screen%20Shot%202018-07-26%20at%203.47.43%20PM.png)

Couldn't find an item that was multi-layered and had files within it, but I think it works as intended.

--------------------------------------------------------------
