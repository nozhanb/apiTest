#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:33:23 2019

@author: nozhan
"""

from matplotlib import colors
import matplotlib.pyplot as plt

def city_map(inputData, height = None, width = None):
    """ This method creates a thematic map of the ROI."""
    
    inputData[inputData == 'b'] = 0
    inputData[inputData == 'c'] = 1
    inputData[inputData == 'g'] = 2
    inputData[inputData == 'l'] = 3
    inputData[inputData == 'r'] = 4
    inputData[inputData == 's'] = 5
    inputData[inputData == 't'] = 6
    inputData[inputData == 'w'] = 7

    inputData = inputData.reshape(height, width)

    cmap = colors.ListedColormap(['red','white','c','yellow','m', 'k', 'green','b'])

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.imshow(inputData.astype('float32'), cmap = cmap)

    fig.savefig('thematicMap.png', bbox_inches='tight', format = 'png')





