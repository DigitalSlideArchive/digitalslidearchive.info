import os, sys, json, glob
import numpy as np
import girder_client
import histomicstk.utils as htk_utils
from cStringIO import StringIO
import io, random
import logging
from os.path import join as opj
from PIL import Image

cohort = "gbm"


logging.getLogger("requests").setLevel(logging.WARNING)
gc = girder_client.GirderClient(apiUrl="http://candygram.neurology.emory.edu:8080/api/v1")

## Connect to girder and get the cohort ID's for all the TCGA collections
tcgaCohorts = gc.get('/tcga/cohort')  ## This gets me the folderID for all the TCGA cohorts
cohortInfo = dict([(x['name'],x['_id']) for x in tcgaCohorts['data']])

slidesInCohort = gc.get('/tcga/cohort/%s/images?limit=%d' % (cohortInfo[cohort],2000))
## PROBABLY should write a generator to grab all the slides instead of just specifying some giant number

### For now I am going to filter out any non DX Cases
dxSlides = [x for x in slidesInCohort['data'] if '-DX' in x['name']]
print(len(dxSlides),"for the %s Cohort"%cohort)

class LinePrinter():
    """
    Print things to stdout on one line dynamically
    """
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

def grabTilesFromImage( imageData, outputDir, lowResMag=1.25, outputRes=20, tilesToOutput=200,debug=False):
    ### This receives a list of images from Girder and will generate tiles and place them in 
    ### Train and Test Directories-- it will split based on train_test_split and also
    ## Will run a low res segmentation step prior to trying to randomly grab tiles from the input stream
    ## outputDir should be something like /data/train/gbm or similar; I'll have the function calling this make sure those
    ## Dirs already exist

    ## Pull the image from girder and then use PIL to turn the raw bytes in an image object
    if debug:
        print("Analyzing %s; pulling base image at %s and outputing tiles at %s" % (imageData['name'],lowResMag,outputRes))
    lowResImg = gc.get('/item/%s/tiles/region?magnification=%s' % ( imageData['_id'], lowResMag),jsonResp=False)    
    lowResPILimage = Image.open(io.BytesIO(lowResImg.content))

    ## Pass the low res image to htk_simple_mask; but first convert to nparray for processing
    im_fgnd_mask_lres = htk_utils.simple_mask(np.asarray(lowResPILimage))

    ### NEXT STEP--- I need to grab every POINT in the MASK.. and then grab 100 Random Tiles...
    ## FIGuRE OUT THE INDEXES OF ALL POINTS IN THE MASK
    (YmaskPts,XmaskPts)  = np.nonzero(im_fgnd_mask_lres)  ## This returns a  Tuples of 2 arrays  X and Y coordinates of non zero points
    ## Zip Y and X into Coords
    maskCoords = zip(YmaskPts,XmaskPts)

    scaleFactor = outputRes/ lowResMag  ### Need to multiply the Y And X coords by this number to get the target coordinates
    maxx = len(maskCoords)
    random.shuffle(maskCoords)  ### shuffle the points and then chose however many pts I wnat to grab tiles for
    # To save the tiles into file
    slideBaseName =  imageData['name'].split(".")[0]

    tilename =[]
    tilecount=0
    for idx, c in enumerate(maskCoords):
        top = c[0]* scaleFactor ## These are scaled to the output res
        left = c[1]* scaleFactor 
        regionWidth = regionHeight = 256

        curTile = gc.get('/item/%s/tiles/region?magnification=%s&top=%d&left=%d&regionWidth=%d&regionHeight=%d' 
                           % ( imageData['_id'], outputRes, top, left,regionWidth,regionHeight),jsonResp=False)
        img = Image.open(io.BytesIO(curTile.content))
        avg = np.average(img)

        status = "Image %s of %s, imgavg:%s" % (idx, maxx,avg)
        if debug:
            LinePrinter(status)

        if avg > 150 and avg < 245:
            tilename = slideBaseName + '_%dx_%d_%d_%dx%d.png' % (outputRes, top, left,regionWidth, regionHeight) 
#            print(outputDir+tilename)
            img.save(opj(outputDir,tilename))
            tilecount+=1

        if tilecount > tilesToOutput or tilecount > maxx:
            break

train  = 0.8
totalSlides = len(dxSlides)
## Output Testing & Training Images for Cohort

for idx,sl in enumerate(dxSlides):
    ## Split into training/test subdirs
#    if( idx/float(totalSlides) < 0.8):
#        opd = "/data/train/%s" % cohort
#    else:
#        opd = "/data/test/%s" % cohort

## I am assuming 80% i.e. 16/20 = 0.8...

    if( (idx % 20)  <  16 ):
        opd = "/data/train/%s" % cohort
    else:
        opd = "/data/test/%s" % cohort

    if not os.path.isdir(opd):
        os.makedirs(opd)


        print("Outputing test set now!!")
    slideBaseName = sl['name'].split(".")[0]
    tilesFound = glob.glob(opd+"/%s*png" %  (slideBaseName))
    #print(tilesDone)

    tilesWanted = 10
    tilesToGenerate = tilesWanted - len(tilesFound)
    #print(tilesToGenerate)
    if (tilesToGenerate) > 0:
        grabTilesFromImage( sl, opd, lowResMag=0.625, outputRes=20, tilesToOutput=tilesToGenerate,debug=True)
    else:
        stats = "Processed %d images" % idx
        LinePrinter(stats)
