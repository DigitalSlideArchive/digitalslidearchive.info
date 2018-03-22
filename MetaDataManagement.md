For a given project/collection we may want to identify a set of tags for an image.  Tags could be important 
properties such as 'Stain', 'SubjectID', 'Region', etc.  These fields can be random strings, but adding a basic
validation schema is important when generating a searchable User Interface.

So for the case of a stain, I want to avoid having  'H&E', 'HE', 'H & E' as distinct stain types, as that makes it extremely
difficult to find anything.  So to create a validation scheme, for a given collection, I am creating a folder called
.ProjectMetadata and in it, I am going to store any documents/PDF's, whatever that may describe the project itself.

Also, this folder is going to have a JSON object called # ProjectScheme that I use to keep track of the properties
I want to validate and/or use for virtual folders.


