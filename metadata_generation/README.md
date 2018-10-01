# Metadata Management

*Last Updated: 1 Oct. 2018*

Instructions for running using docker:
1) Have docker installed.
2) docker run -it -p<localHostPort>:8888 -v <your_dir>:/data/ fgiuste/neuro

Pytesseract is python's wrapper for Google's Tesseract-OCR Engine. Instructions for installing in docker container:
1. $ pip install pytesseract
2. $ su
    * Login to sudo user 
3. $ apt-get update
4. $ apt-get install tesseract-ocr


OCR_REGEX_METADATA_GENERATOR
This script perform optical character recognition (OCR) on slide labels that are pulled from the DSA. Regex is then run on the OCR results and named capturing groups are added as key value pairs to the DSA as item metadata. The script allows a few inputs: 
1) API to work from.
2) Name of collection to get items from.
3) Keys to add to the metadata.
4) Regex string to use in pulling the metadata from OCR output. Note that knowledge of Regex syntax is required and the (?P<capture_group_name> ...) format should be used to get named capture groups. 
5) Ability to override previously found metadata or not.

The output of the script is nothing, instead it pushes the new metadata to the items in the DSA and prints out girder ids of items that failed regex and/or had no valid images. 
