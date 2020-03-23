# File mover
## General info
This example formula copies all files out of a given directory at a source element to a given directory at the destination element.  All of the actions are done via API and can therefore be used with any two elements out of the documentation hub. 

Use this example formula as an example and extend / modify where desired. (ie: add multiple elements)

## Prerequisites
Make sure to have active CE instances created for two different elements from the documentation hub. (Or the same element if you just want to stream files from one folder to another) 

## Expected result
* The formula will scan a given folder for its contents
* The formula will verify if the destination folder (/_data) exists at the destination element
* If the folder does not exists, the formula will create the /_data folder
* Once the /_data folder is available, the formula loops over all content from the folder at the origin and copies it to the /_data folder at the destination (under the same name)

## Example
* Origin folder at Google Drive is called "/myContent" and holds 2 files (1.txt and 2.txt)
* Destination element is dropbox where we are copying files into its root under /_data
* After successful execution, the dropbox account now holds /_data/1.txt and /_data/2.txt
