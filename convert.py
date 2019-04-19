#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 12:18:13 2019

@author: nozhan
"""

import os
#import gdal
import numpy
import affine
import pandas
#import imageio
import rasterio
import numpy.ma

#from scipy.stats import normaltest
#from rasterio.plot import show, show_hist

def data_frame():
    """ The following function will generate a dataFrame with six different columns for each pixel; latitude, longitude, red, green, blue, and infrared bands. Also,
    it generates the height and width of the images (assuming they are the same). The output will be: data, height, widht"""
    count = 0   #   this count is a navie way of introducing the testArray only once. I have to find the right command for it.
    path, direct, files = next(os.walk(os.path.join(os.getcwd(),'uploads')))
    bandList = [f for f in files if os.path.isfile(os.path.join(path, f))]
    for id, bands in enumerate(files):
        band = os.path.join(path,bands)
        bandData   = rasterio.open(band)
        readBand   = bandData.read([1])     #   There is a difference between .read(1) and .read([1]). Will have to look into it later.
        arrayBand  = numpy.transpose(readBand, (1, 2, 0))   #   Changing the order of axis from (band, lat, lon) to (lat, lon , band).
        if count == 0:
            #   We create the testArray to stack them in one array so we can plot data in different bands.
            testArray = numpy.zeros((arrayBand.shape[0], arrayBand.shape[1], 4), dtype = 'float32')
            #   The bandLatLon array is created to put the long and lat values of the coordinates into this array.
            bandLatLon = numpy.zeros((readBand.shape[1], readBand.shape[2], 2), dtype = 'float32')
        bandAff    = bandData.meta['transform']
        width      = bandData.meta['width']
        height     = bandData.meta['height']
        #    bxShift    = 10.54696484 + bandAff[0]/2.   # I am not sure about this line and the line below. They both work!!! Why???
        #   This is where building the new Affine happens.
        bxShift    = bandAff[2] + bandAff[0]/2.
        byShift    = bandAff[5] + bandAff[4]/2.
        bandTrans  = affine.Affine.translation(bxShift, byShift)
        bandScale  = affine.Affine.scale(bandAff[0], bandAff[4])
        bandNewAff = bandTrans * bandScale  #   Remember the order is important!!! bandScale * bandTras is WRONG!!!
        count += 1   #   This line is just the continuation of my navie way of createing an array once in a loop!
        #   This for loop is not the most efficient way of filling the two arrays but it does the job for NOW!!!
        for blat, blon in numpy.ndindex(readBand.shape[1], readBand.shape[2]):
            bandLatLon[blat, blon, :] = bandNewAff * (blon, blat)
            testArray[blat, blon, id] = arrayBand[blat, blon, 0]

    bandDic = {'lat': bandLatLon[:, :, 1].flatten(), 'lon': bandLatLon[:, :, 0].flatten(), \
               'redBand': testArray[:, :, 2].flatten(), \
               'greenBand': testArray[:, :, 1].flatten(), \
               'blueBand': testArray[:, :, 0].flatten(), \
               'irBand': testArray[:, :, 3].flatten()}

    bandFrame = pandas.DataFrame(data = bandDic)

#       bandFrame.to_csv('testTromso.csv', index = False)
    return bandFrame, height, width 
